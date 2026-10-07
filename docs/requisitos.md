# MVP (Minímo Produto Viável) (v1.0)

**Objetivo:** um app funcionando de ponta a ponta, no ar, com testes e README.

## Requisitos Funcionais

| Número | Requisito |
| --- | --- |
| RF01 | O sistema deve permitir que o usuário crie um grupo informando o nome. |
| RF02 | O sistema deve permitir adicionar e remover participantes de um grupo. |
| RF03 | O sistema deve permitir registrar uma despesa informando descrição, valor, quem pagou e quais participantes dividem o valor. |
| RF04 | O sistema deve permitir editar e excluir uma despesa registrada. |
| RF05 | O sistema deve listar todas as despesas do grupo. |
| RF06 | O sistema deve exibir, para cada participante, o total que pagou e o total da sua parte nas despesas. |
| RF07 | O sistema deve exibir o saldo de cada participante, indicando se ele tem valor a receber ou a pagar. |
| RF08 | O sistema deve exibir a lista final de transferências (quem paga quanto a quem) para quitar todas as dívidas com o mínimo de pagamentos possível. |

## Regras de Negócio

| Número | Regra |
| --- | --- |
| RN01 | Toda despesa deve ter valor maior que zero, um pagador que pertença ao grupo e pelo menos um participante na divisão. |
| RN02 | No MVP, o valor da despesa é dividido igualmente entre os participantes selecionados. Por padrão, todos vêm marcados. |
| RN03 | Quando a divisão gerar centavos restantes, eles são distribuídos um a um, seguindo a ordem de cadastro dos participantes, de modo que a soma das partes seja exatamente o valor da despesa. |
| RN04 | Um participante vinculado a alguma despesa não pode ser removido do grupo. |
| RN05 | A soma dos saldos de todos os participantes de um grupo deve ser sempre igual a zero. |
| RN06 | A execução de todas as transferências sugeridas deve zerar o saldo de todos os participantes. |

## Requisitos Não Funcionais

| Número | Requisito |
| --- | --- |
| RNF01 | O sistema deve ser responsivo, funcionando em telas a partir de 360px de largura, sem rolagem horizontal. |
| RNF02 | Os valores devem ser exibidos no formato monetário brasileiro, com duas casas decimais (ex.: R$ 1.234,56). |
| RNF03 | Os valores devem ser armazenados e calculados em centavos (números inteiros). |
| RNF04 | A lógica de cálculo de saldos e transferências deve ser coberta por testes automatizados. |
| RNF05 | O sistema deve exibir mensagens de erro claras quando os dados informados forem inválidos. |
| RNF06 | A aplicação deve estar publicada online, com README documentando como rodar o projeto. |

# Versão 2 (v2.0)

**Objetivo:** transformar o app em algo mais completo e reutilizável.

| Item | Descrição |
| --- | --- |
| Divisão personalizada | Dividir uma despesa por valores ou porcentagens diferentes por participante. |
| Vários grupos | Cada grupo com um link único compartilhável, sem precisar de conta. |
| Acertos de contas | Marcar uma transferência como paga e atualizar os saldos. |
| Histórico | Ver quando cada despesa e cada acerto aconteceram. |
| Exportação | Baixar o resultado final em PDF ou CSV. |
| Gráficos | Gastos por participante, com Chart.js. |
| Login e contas | Opcional, só se sobrar fôlego, por ser a parte mais trabalhosa e a que menos mostra lógica. |