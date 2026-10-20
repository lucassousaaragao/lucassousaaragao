---
name: Perfil GitHub — Lucas Sousa / Luwei
description: Identidade aurora documentada a partir do README e de seus SVGs locais.
colors:
  aurora-violet: "#7B24FF"
  aurora-magenta: "#BF18FF"
  aurora-pink: "#F421A6"
  aurora-orange: "#FF733D"
  aurora-yellow: "#FFBE24"
  hero-background-dark: "#0D0E16"
  hero-background-light: "#F8F6FA"
  hero-text-dark: "#F8F5FF"
  hero-text-light: "#16101F"
  hero-secondary-dark: "#BEB5D0"
  hero-secondary-light: "#665B72"
  card-background-dark: "#101019"
  card-background-light: "#F8F6FC"
  card-text-dark: "#F6F2FC"
  card-text-light: "#171322"
  card-secondary-dark: "#C2BACE"
  card-secondary-light: "#544C60"
  card-border-dark: "#30283D"
  card-border-light: "#DED7E7"
  ribbon-silhouette-dark: "#191524"
  ribbon-silhouette-light: "#E2DCEB"
  ribbon-edge-dark: "#FFE3A0"
  ribbon-edge-light: "#C87718"
typography:
  hero-display-desktop: {fontFamily: "Space Grotesk", fontSize: "88px", fontWeight: 600, letterSpacing: "-0.025em"}
  hero-display-mobile: {fontFamily: "Space Grotesk", fontSize: "76px", fontWeight: 600, letterSpacing: "-0.025em"}
  hero-name-desktop: {fontFamily: "Space Grotesk", fontSize: "49px", fontWeight: 600, letterSpacing: "-0.025em"}
  hero-name-mobile: {fontFamily: "Space Grotesk", fontSize: "48px", fontWeight: 600, letterSpacing: "-0.025em"}
  hero-body-desktop: {fontFamily: "Space Grotesk", fontSize: "26px", fontWeight: 400, letterSpacing: "-0.025em"}
  hero-body-mobile: {fontFamily: "Space Grotesk", fontSize: "25px", fontWeight: 400, letterSpacing: "-0.025em"}
  card-title-desktop: {fontFamily: "Space Grotesk", fontSize: "47px", fontWeight: 700}
  card-title-mobile: {fontFamily: "Space Grotesk", fontSize: "46px", fontWeight: 700}
  card-body-desktop: {fontFamily: "Space Grotesk", fontSize: "27px", fontWeight: 500}
  card-body-mobile: {fontFamily: "Space Grotesk", fontSize: "30px", fontWeight: 500}
  card-action-desktop: {fontFamily: "Space Grotesk", fontSize: "21px", fontWeight: 600}
  card-action-mobile: {fontFamily: "Space Grotesk", fontSize: "26px", fontWeight: 600}
rounded: {product-card: "16px"}
components:
  hero-dark: {backgroundColor: "{colors.hero-background-dark}", textColor: "{colors.hero-text-dark}"}
  hero-light: {backgroundColor: "{colors.hero-background-light}", textColor: "{colors.hero-text-light}"}
  product-card-dark: {backgroundColor: "{colors.card-background-dark}", textColor: "{colors.card-text-dark}", rounded: "{rounded.product-card}"}
  product-card-light: {backgroundColor: "{colors.card-background-light}", textColor: "{colors.card-text-light}", rounded: "{rounded.product-card}"}
---

# Design System: Perfil GitHub — Lucas Sousa / Luwei

## Overview

**Creative North Star: "Aurora em movimento"**

Rótulo descritivo da implementação existente: composição editorial clara, tipografia expressiva e geometrias nas cores aurora. Este documento registra a extensão da identidade preservada em `assets/aurora-personal.svg`; não propõe outra identidade.

Escopo: imagens do README e organização do conteúdo. A página, a fonte do Markdown e os estados de links são controlados pelo GitHub. Fontes de extração: `PRODUCT.md`, `README.md`, `scripts/generate_hero.py`, `scripts/generate_cards.py` e `assets/SOURCES.md`. O registro não certifica a renderização no GitHub.

**Key Characteristics:**

- Nome pessoal em destaque, chamada em duas linhas e texto de apoio legível.
- Aurora compartilhada entre hero e produtos; fundos claros e escuros próprios.
- SVGs locais autossuficientes, movimento finito e conteúdo equivalente em texto.

## Colors

**Primary:** a paleta aurora oficial já presente no repositório reúne violeta, magenta, rosa, laranja e amarelo (`aurora-*`). Ela percorre a fita do hero, o pequeno traço sob o nome e as geometrias dos produtos, sem substituir as marcas.

**Neutral:** os pares `hero-background-*` e `card-background-*` definem os fundos das imagens; `*-text-*` atende títulos e ações, e `*-secondary-*` atende descrições. Os sufixos `dark` e `light` identificam a variante da imagem, não a luminosidade da cor isolada. `card-border-*` delimita os cards; `ribbon-silhouette-*` e `ribbon-edge-*` dão estrutura e acabamento à fita.

## Typography

**Display Font:** Space Grotesk, fonte variável local em `assets/fonts/SpaceGrotesk.ttf`, licenciada em `assets/fonts/OFL.txt`.
**Body Font:** a tipografia nativa do GitHub no Markdown; Space Grotesk somente dentro das imagens.

Os geradores convertem os glifos dos SVGs em paths. Não há carregamento remoto de fonte nem dependência de fallback para essas imagens. Os tamanhos do frontmatter são unidades do SVG, escaladas com a imagem; não equivalem a tamanhos CSS fixos na página.

### Hierarchy

`hero-name-*` identifica Lucas; `hero-display-*` apresenta “Construo o próximo.”; `hero-body-*` explica a atuação. Nos cards, `card-title-*`, `card-body-*` e `card-action-*` distinguem produto, proposta e destino. O hero posiciona linhas por baseline; os cards usam o avanço natural dos glifos. Nenhuma escala de `line-height` do Markdown é definida aqui.

## Layout

| Imagem | Desktop | Mobile |
| :--- | :--- | :--- |
| Hero | 1200 × 560 | 680 × 760 |
| Cards Flow / Dev | 1200 × 240 | 680 × 360 |

Cada `<picture>` seleciona mobile em `(max-width: 767px)`, combinado primeiro com `(prefers-color-scheme: dark)`; segue mobile claro, desktop escuro e fallback claro em `<img width="100%">`. As variantes são arquivos próprios, não recortes de uma imagem única.

O hero põe texto à esquerda e fita à direita no desktop; no mobile, a fita ocupa a região inferior. Os cards reorganizam descrições em duas linhas no mobile. As coordenadas são composições dos geradores; não há grid CSS nem escala geral de espaçamento. O corpo segue uma coluna de Markdown com títulos, parágrafos, navegação, produtos e tabela em `<details open>`.

## Elevation & Depth

Os SVGs não usam sombras CSS nem filtros de desfoque. A profundidade vem da fita tridimensional projetada, das sobreposições dos traços e de uma silhueta estrutural com espessura de 28 unidades e opacidade de 0,62. Cards usam fundo tonal e contorno simples.

## Shapes

O hero tem fundo retangular sem arredondamento. Cards usam o token `product-card`, borda de uma unidade e seta diagonal de duas unidades com terminações arredondadas. A fita reúne 44 traços e uma linha de acabamento; Flow usa 15 curvas e Dev usa 32 elipses. Essas geometrias não são logotipos.

## Components

### Hero

`assets/hero-{dark,light}.svg` e `assets/hero-mobile-{dark,light}.svg` contêm nome, chamada, descrição e fita aurora.
As 44 curvas coloridas permanecem completas desde o primeiro instante e não recebem animação de traçado.
Somente a linha luminosa extra da borda recebe `reveal`; uma captura do quadro inicial preserva a fita inteira.
`turn` gira o grupo de −9° a 0°; o conjunto permanece estático ao final.
Ambas as animações duram **4,8 s, uma iteração**, com `cubic-bezier(.16,1,.3,1)` e preenchimento `both`.
`prefers-reduced-motion: reduce` desliga ambas. O desenho completo continua disponível sem animação.

### Cards / Containers

`assets/flow-*.svg` e `assets/dev-*.svg` oferecem variantes de tamanho e tema. São imagens estáticas envolvidas por links para os produtos; as ações desenhadas fazem parte da imagem. Título, proposta, geometria e seta seguem a hierarquia extraída. Não há estados próprios de hover, foco ou pressão implementados no SVG.

### Navigation

Links centrais usam âncoras do README e o site Luwei. As seções, a tabela de tecnologias e o `<details open>` permanecem nativos do GitHub, incluindo interação e aparência. O rodapé preserva `assets/luwei-official.png`, cópia original da logo pública, exibida a 180 px, e a assinatura institucional.

## Do's and Don'ts

### Do:

- **Do** preservar a aurora, a logo original e as variantes locais de tamanho e tema.
- **Do** manter `alt`, `<title>`, `<desc>` e texto equivalente no README ao editar imagens.
- **Do** conservar a animação finita e a preferência por movimento reduzido ao regenerar o hero.

### Don't:

- **Don't** atribuir ao projeto fontes, controles, sombras ou estados que pertencem à página do GitHub.
- **Don't** substituir a logo por geometrias dos cards nem introduzir fontes ou imagens remotas nos SVGs.
- **Don't** adicionar JavaScript, iframes ou CSS destinado à página do README.

**Regeneração:** executar na raiz do repositório; `scripts/requirements.txt` fixa `fonttools==4.61.1`. Os dois geradores reescrevem as quatro variantes de hero e as oito variantes de cards. Atualizar este documento e o sidecar após mudanças nesses arquivos.

```bash
python -m pip install -r scripts/requirements.txt
python scripts/generate_hero.py
python scripts/generate_cards.py
```
