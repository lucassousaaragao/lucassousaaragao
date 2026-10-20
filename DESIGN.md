---
name: Perfil GitHub — Lucas Sousa / Luwei
description: Identidade de engenharia com código, stack visual e marcas originais.
colors:
  aurora-violet: "#7B24FF"
  aurora-magenta: "#BF18FF"
  aurora-pink: "#F421A6"
  aurora-orange: "#FF733D"
  aurora-yellow: "#FFBE24"
  background-dark: "#080C16"
  background-light: "#F4F6FC"
  foreground-dark: "#F4F7FC"
  foreground-light: "#121A2B"
  secondary-dark: "#A6B5CA"
  secondary-light: "#51617A"
  line-dark: "#243047"
  line-light: "#D4DCEA"
  code-dark: "#C6D1E4"
  code-light: "#243C60"
  keyword-dark: "#DCAAFF"
  keyword-light: "#7125B9"
  string-dark: "#FFBA86"
  string-light: "#99400C"
  punctuation-dark: "#8FA4C3"
  punctuation-light: "#566B89"
  project-plate-light: "#FFFFFF"
  dev-plate-dark: "#060611"
typography:
  hero-name-desktop: {"fontFamily": "Sora", "fontSize": "105px", "fontWeight": 650, "letterSpacing": "-0.032em"}
  hero-name-mobile: {"fontFamily": "Sora", "fontSize": "79px", "fontWeight": 650, "letterSpacing": "-0.032em"}
  hero-role: {"fontFamily": "Sora", "fontSize": "30px", "fontWeight": 550, "letterSpacing": "-0.012em"}
  hero-founder: {"fontFamily": "Sora", "fontSize": "23px", "fontWeight": 400, "letterSpacing": "-0.012em"}
  hero-code-desktop: {"fontFamily": "JetBrains Mono", "fontSize": "21px", "fontWeight": 400, "letterSpacing": "0em"}
  hero-code-mobile: {"fontFamily": "JetBrains Mono", "fontSize": "23px", "fontWeight": 400, "letterSpacing": "0em"}
  stack-heading: {"fontFamily": "Sora", "fontSize": "32px", "fontWeight": 600}
  stack-label-desktop: {"fontFamily": "Sora", "fontSize": "21px", "fontWeight": 500}
  stack-label-mobile: {"fontFamily": "Sora", "fontSize": "24px", "fontWeight": 500}
  project-title-desktop: {"fontFamily": "Sora", "fontSize": "31px", "fontWeight": 600, "letterSpacing": "-0.012em"}
  project-title-mobile: {"fontFamily": "Sora", "fontSize": "29px", "fontWeight": 600, "letterSpacing": "-0.012em"}
  project-title-long: {"fontFamily": "Sora", "fontSize": "27px", "fontWeight": 600, "letterSpacing": "-0.012em"}
  project-body-desktop: {"fontFamily": "Sora", "fontSize": "21px", "fontWeight": 400, "letterSpacing": "-0.012em", "lineHeight": 1.4}
  project-body-mobile: {"fontFamily": "Sora", "fontSize": "23px", "fontWeight": 400, "letterSpacing": "-0.012em", "lineHeight": 1.4}
rounded: {project-logo: "8px", stack-logo: "12px"}
components:
  hero-dark: {"backgroundColor": "{colors.background-dark}", "textColor": "{colors.foreground-dark}"}
  hero-light: {"backgroundColor": "{colors.background-light}", "textColor": "{colors.foreground-light}"}
  stack-dark: {"backgroundColor": "{colors.background-dark}", "textColor": "{colors.foreground-dark}"}
  stack-light: {"backgroundColor": "{colors.background-light}", "textColor": "{colors.foreground-light}"}
  project-logo-plate: {"backgroundColor": "{colors.project-plate-light}", "rounded": "{rounded.project-logo}"}
---
# Design System: Perfil GitHub — Lucas Sousa / Luwei

## Overview

**Creative North Star: "Engenharia Luwei em aurora"**

A identidade põe Lucas Sousa e sua atuação em engenharia no centro. O código real de `profile.ts`, os alinhamentos de um editor e as marcas originais conduzem a composição. A paleta aurora permanece como assinatura gráfica; os símbolos de programação dão forma ao traço que conecta os elementos.

O redesign responde ao pedido de mais programação, futurismo e presença visual da stack. Substitui a direção anterior de fita abstrata por uma composição baseada em código. Este documento descreve a implementação atual dos SVGs e do README; não certifica a renderização final no GitHub.

**Key Characteristics:**

- Nome e profissão com hierarquia forte; código real com destaque sintático.
- 55 tecnologias em seis grupos, com logos-fonte e nomes completos.
- Oito projetos com marcas fornecidas pelo proprietário, sem redesenho das logos.
- Composições próprias para desktop e mobile, em temas claro e escuro.
- Um movimento finito no hero; conteúdo e traço-base visíveis desde o primeiro quadro.

## Colors

### Primary

A paleta `aurora-*` reúne violeta, magenta, rosa, laranja e amarelo. Ela percorre a estrutura do hero e os pequenos segmentos que iniciam as divisórias da stack. Não é aplicada ao texto corrente nem usada para recolorir marcas de terceiros.

### Neutral

`background-*`, `foreground-*`, `secondary-*` e `line-*` formam os pares de superfície, texto, apoio e divisórias. Os sufixos indicam a variante da imagem. No código, `code-*`, `keyword-*`, `string-*` e `punctuation-*` distinguem tokens sem simular uma execução.

As logos conservam suas cores. `project-plate-light` oferece um campo branco às marcas que precisam dele; a versão escura do painel também usa suportes claros para ícones monocromáticos. A logo LuweiDev conserva seu fundo próprio.

## Typography

**Display Font:** Sora, local, convertida em paths dentro dos SVGs.

**Code Font:** JetBrains Mono, usada no trecho de TypeScript, no nome do arquivo e na numeração das linhas.

**Body Font:** a fonte nativa do GitHub no Markdown. O projeto não altera a tipografia da página hospedada.

Os tamanhos do frontmatter são unidades do SVG. Eles escalam proporcionalmente com a largura da imagem e não constituem tamanhos CSS fixos na página. Cada glifo é definido uma vez por variante tipográfica e reaproveitado com `xlink:href`.

### Hierarchy

- `hero-name-*`: nome em duas linhas; maior nível da apresentação.
- `hero-role` e `hero-founder`: profissão e vínculo com a Luwei.
- `hero-code-*`: conteúdo extraído diretamente de `profile.ts`, com baselines separados por 35 unidades no desktop e 32 no mobile.
- `stack-heading` e `stack-label-*`: áreas técnicas e nomes das tecnologias. Nomes longos podem ocupar duas linhas.
- `project-title-*` e `project-body-*`: nomes e legendas; o título longo de Perícia Paraíba recebe duas linhas próprias.

## Layout

| Painel | Desktop | Mobile |
| :--- | :--- | :--- |
| Hero | 1200 × 620 | 600 × 800 |
| Stack | 1200 × 1528; oito colunas | 600 × 3342; três colunas |
| Projetos | 1200 × 980; duas colunas | 600 × 1640; uma coluna |

O README usa `<picture>` com o breakpoint `(max-width: 767px)`. A ordem é mobile escuro, mobile claro, desktop escuro e fallback claro. Cada imagem tem largura fluida; os arquivos mobile recompõem o conteúdo.

No desktop, nome e apresentação ocupam o lado esquerdo do hero; código e marca ocupam o direito. No mobile, identidade e código ficam em sequência vertical. A stack usa bandas por categoria, células abertas e espaçamento entre nomes. Seus itens têm passo vertical de 118 unidades no desktop e 128 no mobile; as margens horizontais são 44 e 28, respectivamente.

O diretório de projetos usa divisórias e uma área contida para cada logo. As imagens preservam proporção. Os links públicos ficam no Markdown após o painel; não há botões desenhados dentro das imagens. Stack e projetos têm equivalentes textuais em `<details>` fechados inicialmente.

## Elevation & Depth

Os painéis são planos. A hierarquia resulta de contraste, escala, alinhamento e divisórias, sem sombras ou filtros de desfoque. O brilho já existente em algumas logos pertence ao arquivo original da marca e não define um efeito global.

## Shapes

A moldura aberta do hero tem um canto chanfrado. Chaves, recuos e linhas de código orientam a geometria aurora. A linha animada acompanha um traço-base sempre visível.

Os suportes de logos têm cantos de 8 unidades no diretório e 12 na stack. Eles existem onde o contraste da marca pede uma superfície própria. As células técnicas e as entradas do diretório permanecem abertas, separadas por linhas finas.

## Components

### Hero com código

`assets/hero-{dark,light}.svg` e `assets/hero-mobile-{dark,light}.svg` são gerados por `scripts/generate_profile.py`. Nome, profissão e foco aparecem no primeiro quadro. O código é uma declaração de perfil que existe em `profile.ts`; não representa logs, disponibilidade ou resultados de execução.

Somente o destaque `.trace` se move: 4,8 segundos, uma execução, curva `cubic-bezier(.16,1,.3,1)`, término estático. `prefers-reduced-motion: reduce` desliga a animação e mantém a composição. A stack e o diretório são estáticos.

### Stack de engenharia

`assets/stack-{dark,light}.svg` e `assets/stack-mobile-{dark,light}.svg` são gerados por `scripts/generate_stack.py`. O inventário público em `scripts/stack.json` contém 55 nomes e 53 logos-fonte distintos. Codex compartilha a marca OpenAI; Claude Code compartilha a marca Anthropic. Tiptap e React Flow usam as marcas de seus sites oficiais.

Os grupos são Linguagens; Interfaces e desktop; Backend e dados; Cloud e entrega; IA e integrações; Qualidade. IDs e classes dos SVGs incorporados recebem prefixos para evitar colisões. Nenhuma barra ou selo indica suposto domínio de uma tecnologia.

### Diretório de projetos

`assets/projects-{dark,light}.svg` e `assets/projects-mobile-{dark,light}.svg` são gerados por `scripts/generate_profile.py`. A composição reúne Luwei Flow, LuweiDev, Zênit, Horora, CuidarPro, eAudit, Projeto Perícia Paraíba e Union.

As cópias para a web preservam geometria e cores das marcas; apenas margens vazias e escala proporcional são ajustadas. O inventário de origem e transformações está em `assets/projects/SOURCES.json`. As descrições seguem o conteúdo público disponível; eAudit e Union são apresentados somente pelo nome.

### Navegação e leitura

Links, títulos, listas, tabelas e `<details>` usam os controles nativos do GitHub. O repositório não define hover, foco, scrollbar, campos, estados de carregamento ou CSS da página. `alt`, `<title>`, `<desc>` e conteúdo em Markdown dão acesso à informação além das imagens.

## Do's and Don'ts

### Do

- **Do** manter nome, profissão, marcas originais, princípios e assinatura da Luwei.
- **Do** editar o conteúdo de código em `profile.ts` e regenerar o hero.
- **Do** manter o inventário visual alinhado à lista textual do README.
- **Do** preservar nomes completos, proporções, contraste e licenças das marcas.
- **Do** manter versões mobile próprias, movimento finito e alternativa de movimento reduzido.

### Don't

- **Don't** transformar a fita abstrata anterior na direção ativa deste redesign.
- **Don't** simular execução, terminal, disponibilidade, métricas, níveis de domínio ou resultados.
- **Don't** inventar links, descrições de produtos ou símbolos para tecnologias sem logo-fonte.
- **Don't** incorporar JavaScript, iframes ou CSS para controlar a página do GitHub.
- **Don't** tornar conteúdo essencial dependente da animação ou de fontes externas.
