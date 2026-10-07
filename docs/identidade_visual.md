# Guia de Estilos e Especificações — Splito

## Cores Principais

| Uso | Nome da Cor | Código Hex |
| :--- | :--- | :--- |
| **Azul-escuro principal** | Navy | `#102A43` |
| **Azul-escuro secundário** | Navy 2 | `#173F5F` |
| **Verde-água principal** | Aqua | `#16B8A6` |
| **Verde-água escuro** | Aqua Dark | `#0C9487` |
| **Verde-água claro** | Aqua Soft | `#E8F8F5` |
| **Branco** | Surface | `#FFFFFF` |
| **Fundo da aplicação** | Canvas | `#F5F7F9` |
| **Fundo externo do protótipo** | Cinza azulado | `#DFE6EC` |
| **Texto principal** | Azul profundo | `#12253F` |
| **Texto secundário** | Cinza azulado | `#6C7C8E` |
| **Bordas e divisórias** | Cinza claro | `#E6EBEF` |
| **Azul claro auxiliar** | Blue Soft | `#EDF5FF` |

---

### Gradientes

* **Card de Total:** `#123451` → `#18526D`
* **Card de Resultados:** `#133752` → `#185A70`
* **Barras de Progresso:** `#16B8A6` → `#54D3C4`

---

### Cores de Feedback

| Estado | Cor do Texto | Cor do Fundo |
| :--- | :--- | :--- |
| **Positivo / Pago** | `#087E70` | `#E8F8F5` |
| **Valor devido** | `#BA6633` | `#FFF0E6` |
| **Aviso âmbar** | `#D48A2E` | `#FFF6E9` |
| **Destaque azul** | `#3976C5` | `#EDF5FF` |

---

### Avatares

| Pessoa | Cor do Texto | Cor do Fundo |
| :--- | :--- | :--- |
| **Gabriel** | `#2A64AE` | `#DCEAFF` |
| **Mariana** | `#087F75` | `#CCF3ED` |
| **Lucas** | `#7450A7` | `#ECE1FF` |
| **Bia** | `#B55D23` | `#FFE5D2` |

---

### Sombras

```css
box-shadow: 0 14px 40px rgba(29, 55, 78, 0.08);
```

## Tipografia

A fonte utilizada no projeto é a **Inter**, importada via Google Fonts.

### Pesos Utilizados

- **Regular**: 400
- **Medium**: 500
- **SemiBold**: 600
- **Bold**: 700
- **ExtraBold**: 800

```css
@import url("[https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap](https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap)");

body {
  font-family: "Inter", sans-serif;
}

```

