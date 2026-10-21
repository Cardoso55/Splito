-- ============================================================
-- Splito - schema do banco (gerado a partir do DER)
-- Dialeto: SQLite (para PostgreSQL, veja as notas no final)
-- Valores monetários sempre em CENTAVOS (INTEGER) para evitar
-- erros de ponto flutuante: R$ 12,50 => 1250
-- ============================================================

PRAGMA foreign_keys = ON;

-- ------------------------------------------------------------
-- USUARIO: conta de login (V2). Um usuário pode estar em vários grupos.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome        TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE,
    senha_hash  TEXT    NOT NULL,
    criado_em   TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- GRUPO
-- criado_por_participante_id_fk é NULLABLE de propósito: grupo e
-- participante se referenciam (dependência circular). Fluxo:
--   1) INSERT grupo (criador NULL)
--   2) INSERT participante (admin)
--   3) UPDATE grupo SET criado_por_participante_id_fk = <id>
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS grupo (
    id_grupo                       INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                           TEXT    NOT NULL,
    descricao                      TEXT,
    codigo_convite                 TEXT    NOT NULL UNIQUE,
    criado_por_participante_id_fk  INTEGER,
    criado_em                      TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (criado_por_participante_id_fk)
        REFERENCES participante (id_participante)
        ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- PARTICIPANTE: a pessoa DENTRO de um grupo (entidade associativa
-- entre GRUPO e USUARIO).
-- usuario_id_fk é NULLABLE para permitir que o admin adicione
-- pessoas só pelo nome (RF02), sem exigir conta. Se quiser seguir
-- o DER à risca (1,1), troque para NOT NULL.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS participante (
    id_participante  INTEGER PRIMARY KEY AUTOINCREMENT,
    grupo_id_fk      INTEGER NOT NULL,
    usuario_id_fk    INTEGER,
    nome_exibicao    TEXT    NOT NULL,
    criado_em        TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grupo_id_fk)   REFERENCES grupo (id_grupo)      ON DELETE CASCADE,
    FOREIGN KEY (usuario_id_fk) REFERENCES usuario (id_usuario)  ON DELETE SET NULL,
    -- o mesmo usuário não entra duas vezes no mesmo grupo
    UNIQUE (grupo_id_fk, usuario_id_fk)
);

-- ------------------------------------------------------------
-- DESPESA
-- tipo_divisao prepara a V2 (no MVP é sempre 'igual').
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS despesa (
    id_despesa                  INTEGER PRIMARY KEY AUTOINCREMENT,
    grupo_id_fk                 INTEGER NOT NULL,
    pagador_participante_id_fk  INTEGER NOT NULL,
    descricao                   TEXT    NOT NULL,
    valor_centavos              INTEGER NOT NULL CHECK (valor_centavos > 0),
    data_despesa                TEXT    NOT NULL,              -- 'YYYY-MM-DD'
    tipo_divisao                TEXT    NOT NULL DEFAULT 'igual'
                                CHECK (tipo_divisao IN ('igual', 'valor_exato', 'percentual')),
    criado_em                   TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grupo_id_fk)
        REFERENCES grupo (id_grupo) ON DELETE CASCADE,
    FOREIGN KEY (pagador_participante_id_fk)
        REFERENCES participante (id_participante) ON DELETE RESTRICT
);

-- ------------------------------------------------------------
-- DIVISAO: quanto de cada despesa cabe a cada participante
-- (entidade associativa entre DESPESA e PARTICIPANTE).
-- A soma de valor_centavos das divisões deve ser igual ao
-- valor_centavos da despesa -> validar no backend (Python).
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS divisao (
    id_divisao          INTEGER PRIMARY KEY AUTOINCREMENT,
    despesa_id_fk       INTEGER NOT NULL,
    participante_id_fk  INTEGER NOT NULL,
    valor_centavos      INTEGER NOT NULL CHECK (valor_centavos >= 0),
    FOREIGN KEY (despesa_id_fk)
        REFERENCES despesa (id_despesa) ON DELETE CASCADE,
    FOREIGN KEY (participante_id_fk)
        REFERENCES participante (id_participante) ON DELETE RESTRICT,
    UNIQUE (despesa_id_fk, participante_id_fk)
);

-- ------------------------------------------------------------
-- ACERTO: pagamento real entre dois participantes para quitar dívida.
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS acerto (
    id_acerto            INTEGER PRIMARY KEY AUTOINCREMENT,
    grupo_id_fk          INTEGER NOT NULL,
    de_participante_fk   INTEGER NOT NULL,   -- quem paga
    para_participante_fk INTEGER NOT NULL,   -- quem recebe
    valor_centavos       INTEGER NOT NULL CHECK (valor_centavos > 0),
    data_acerto          TEXT    NOT NULL,   -- 'YYYY-MM-DD'
    status               TEXT    NOT NULL DEFAULT 'pendente'
                         CHECK (status IN ('pendente', 'confirmado')),
    criado_em            TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grupo_id_fk)
        REFERENCES grupo (id_grupo) ON DELETE CASCADE,
    FOREIGN KEY (de_participante_fk)
        REFERENCES participante (id_participante) ON DELETE RESTRICT,
    FOREIGN KEY (para_participante_fk)
        REFERENCES participante (id_participante) ON DELETE RESTRICT,
    CHECK (de_participante_fk <> para_participante_fk)
);

-- ------------------------------------------------------------
-- ÍNDICES nas chaves estrangeiras mais consultadas
-- ------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_participante_grupo   ON participante (grupo_id_fk);
CREATE INDEX IF NOT EXISTS idx_participante_usuario ON participante (usuario_id_fk);
CREATE INDEX IF NOT EXISTS idx_despesa_grupo        ON despesa (grupo_id_fk);
CREATE INDEX IF NOT EXISTS idx_despesa_pagador      ON despesa (pagador_participante_id_fk);
CREATE INDEX IF NOT EXISTS idx_divisao_despesa      ON divisao (despesa_id_fk);
CREATE INDEX IF NOT EXISTS idx_divisao_participante ON divisao (participante_id_fk);
CREATE INDEX IF NOT EXISTS idx_acerto_grupo         ON acerto (grupo_id_fk);

-- ============================================================
-- NOTAS PARA PORTAR PARA POSTGRESQL
--  * INTEGER PRIMARY KEY AUTOINCREMENT -> GENERATED ALWAYS AS IDENTITY
--  * TEXT de data/hora -> DATE / TIMESTAMPTZ DEFAULT now()
--  * Remover o PRAGMA
--  * A FK circular grupo <-> participante exige criar 'grupo' sem a FK
--    e adicioná-la depois com ALTER TABLE ... ADD CONSTRAINT
-- ============================================================