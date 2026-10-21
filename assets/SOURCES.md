# Fontes dos recursos visuais

As cópias PNG distribuídas no repositório passam por `scripts/sanitize_logos.py`, que remove metadados de documentos e mantém os pixels, a transparência e as cores. Perfis sRGB redundantes também são removidos quando uma conversão comprova a identidade dos pixels. A verificação compara a imagem antes e depois. Os arquivos de origem do proprietário ficam fora desse processo.

## Logos da Luwei e dos projetos

Os arquivos em `projects/` foram fornecidos pelo proprietário para este README. A seleção inclui a Luwei Software House e oito projetos: Luwei Flow, LuweiDev, Zênit, Horora, CuidarPro, eAudit, Projeto Perícia Paraíba e Union.

`projects/SOURCES.json` registra os arquivos importados, seus hashes e as operações usadas nas cópias de `projects/web/`. As cópias para exibição mantêm a proporção e as cores das marcas; recebem apenas retirada de margens vazias e redução proporcional. Os arquivos importados são preservados. As marcas continuam pertencendo aos respectivos titulares.

A marca da empresa usada no redesign foi fornecida pelo proprietário e está em `projects/luwei.png`.

## Logos das tecnologias

O inventário de exibição está em `../scripts/stack.json`: 55 nomes, 53 arquivos de logo distintos. As fontes originais ficam em `stack/`, com URLs, revisões, hashes e licenças em `stack/SOURCES.json`.

- Devicon: licença em `stack/DEVICON-LICENSE.txt`.
- Simple Icons: licença em `stack/SIMPLE-ICONS-LICENSE.txt`.
- PHPUnit: licença em `stack/PHPUNIT-LICENSE.txt`.
- OpenAI: ativo da página oficial de marca; condições registradas em `stack/OPENAI-USAGE.md`.

As licenças dos repositórios não substituem os direitos e as orientações de uso das marcas. Os SVGs de origem conservam suas cores e geometria. Ao incorporá-los aos painéis, o gerador aplica escala proporcional e prefixos aos IDs e classes para evitar conflitos.

Codex usa a marca OpenAI; Claude Code usa a marca Anthropic. As marcas Tiptap e React Flow vêm dos sites oficiais [tiptap.dev](https://tiptap.dev/) e [reactflow.dev](https://reactflow.dev/), com a origem exata registrada no inventário de fontes.

## Tipografia

| Fonte | Origem | Blob Git | Licença local |
| :--- | :--- | :--- | :--- |
| Sora | [Google Fonts — Sora](https://github.com/google/fonts/blob/main/ofl/sora/Sora%5Bwght%5D.ttf) | `3b93d661fa07f5948799ba29979009b409cd4740` | `fonts/Sora-OFL.txt` |
| JetBrains Mono | [Google Fonts — JetBrains Mono](https://github.com/google/fonts/blob/main/ofl/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf) | `aa310be8b717fe3774f9444dd89d5f4101cc6d10` | `fonts/JetBrainsMono-OFL.txt` |

As fontes variáveis ficam em `fonts/`. O novo hero usa Sora para identidade e JetBrains Mono para código. Stack e diretório usam Sora. Os geradores convertem os glifos em paths e reaproveitam suas definições; as imagens não carregam fontes remotas.

## Composição e geração

Hero e diretório: `../scripts/generate_profile.py`. Stack: `../scripts/generate_stack.py`. O código exibido é lido de `../profile.ts`; o inventário textual da stack é gerado em `../scripts/stack.json`.

Para regenerar a partir da raiz do repositório:

```sh
python -m pip install -r requirements-design.txt
python scripts/generate_profile.py
python scripts/generate_stack.py
```

Os SVGs são autossuficientes, com imagens locais incorporadas, sem recursos remotos ou scripts. A linha do hero usa animação CSS interna e finita, com suporte a movimento reduzido. O restante permanece estático.

`aurora-personal.svg` é o banner histórico já existente no repositório e foi preservado.
