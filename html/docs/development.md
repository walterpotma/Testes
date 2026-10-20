# 🛠️ Guia de Desenvolvimento

## Configuração do Ambiente

### Pré-requisitos
- **Node.js** (opcional, para ferramentas de desenvolvimento)
- **Python** (para servidor local simples)
- **Git** (para controle de versão)
- **Editor de código** (VS Code recomendado)

### Extensões Recomendadas (VS Code)
```json
{
  "recommendations": [
    "ms-vscode.vscode-json",
    "bradlc.vscode-tailwindcss",
    "esbenp.prettier-vscode",
    "ms-vscode.live-server",
    "ritwickdey.liveserver"
  ]
}
```

## Estrutura de Desenvolvimento

### 1. **Organização de Arquivos**
```
public/
├── index.html              # Página principal
├── [guia].html            # Páginas dos guias
└── assets/
    ├── css/
    │   ├── global.css      # Variáveis e estilos globais
    │   ├── index.css       # Estilos da página inicial
    │   └── [guia].css      # Estilos específicos por guia
    ├── js/
    │   ├── index.js        # Lógica da página inicial
    │   └── [guia].js       # Lógica específica por guia
    └── images/            # Imagens e ícones
```

### 2. **Padrões de Código**

#### HTML
- Use **HTML5 semântico**
- **Acessibilidade** (ARIA labels, alt texts)
- **SEO** (meta tags, structured data)
- **Performance** (lazy loading, preload)

#### CSS
- **Variáveis CSS** para cores e espaçamentos
- **Mobile-first** approach
- **BEM methodology** para classes
- **Flexbox/Grid** para layouts

#### JavaScript
- **ES6+** features
- **Modular** structure
- **Event delegation**
- **Performance** (debounce, throttle)

## Adicionando um Novo Guia

### 1. **Criar Estrutura Básica**
```bash
# Criar arquivos
touch public/novo-guia.html
touch public/assets/css/novo-guia.css
touch public/assets/js/novo-guia.js
```

### 2. **Template HTML**
```html
<!DOCTYPE html>
<html lang="pt-BR" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guia Interativo do [Tema]</title>
    <link rel="stylesheet" href="assets/css/global.css">
    <link rel="stylesheet" href="assets/css/novo-guia.css">
    <script src="assets/js/novo-guia.js"></script>
</head>
<body class="bg-warm-beige text-charcoal">
    <!-- Conteúdo do guia -->
</body>
</html>
```

### 3. **Template CSS**
```css
@import url('./global.css');

/* Estilos específicos do guia */
.main-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

/* Responsive */
@media (min-width: 768px) {
    .main-container {
        flex-direction: row;
    }
}
```

### 4. **Template JavaScript**
```javascript
document.addEventListener('DOMContentLoaded', () => {
    // Navegação por seções
    const sections = document.querySelectorAll('main section');
    const navLinks = document.querySelectorAll('.sidebar-link');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href').substring(1) === entry.target.id) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, { rootMargin: '-50% 0px -50% 0px' });

    sections.forEach(section => {
        observer.observe(section);
    });
});
```

## Padrões de Design

### 1. **Cores (Variáveis CSS)**
```css
:root {
    --warm-beige: #F7F3E9;
    --charcoal: #36454F;
    --terracotta: #E07A5F;
    --stone-200: #E7E5E4;
    --stone-300: #D6D3D1;
}
```

### 2. **Tipografia**
```css
body {
    font-family: 'Inter', sans-serif;
}

.font-mono {
    font-family: 'Roboto Mono', monospace;
}
```

### 3. **Layout**
```css
.main-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.sidebar {
    width: 100%;
    background-color: var(--stone-200);
    padding: 1rem;
}

.main-content {
    flex: 1;
    margin-left: 0;
    padding: 1rem;
}
```

## Ferramentas de Desenvolvimento

### 1. **Servidor Local**
```bash
# Python
cd public
python -m http.server 8000

# Node.js (com live-reload)
npx live-server public

# PHP
cd public
php -S localhost:8000
```

### 2. **Linting e Formatação**
```bash
# Prettier (formatação)
npx prettier --write "public/**/*.{html,css,js}"

# ESLint (JavaScript)
npx eslint "public/assets/js/**/*.js"
```

### 3. **Otimização de Imagens**
```bash
# ImageOptim (macOS)
# TinyPNG (online)
# Squoosh (Google)
```

## Testes

### 1. **Testes Manuais**
- [ ] Responsividade em diferentes dispositivos
- [ ] Funcionalidade em diferentes navegadores
- [ ] Acessibilidade (screen readers)
- [ ] Performance (Lighthouse)

### 2. **Ferramentas de Teste**
```bash
# Lighthouse (performance)
npx lighthouse http://localhost:8000 --view

# Acessibilidade
npx axe-core http://localhost:8000
```

## Deploy

### 1. **Desenvolvimento**
```bash
# Servidor local
cd public
python -m http.server 8000
```

### 2. **Produção**
```bash
# Docker
docker build -t resumos-docs .
docker run -p 80:80 resumos-docs

# Nginx
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo nginx -t && sudo systemctl reload nginx
```

## Debugging

### 1. **Console do Navegador**
```javascript
// Debug de JavaScript
console.log('Debug info:', data);

// Debug de CSS
element.style.border = '2px solid red';
```

### 2. **Ferramentas de Desenvolvimento**
- **Chrome DevTools**
- **Firefox Developer Tools**
- **Safari Web Inspector**

## Contribuição

### 1. **Fluxo de Trabalho**
```bash
# Fork do repositório
git clone [seu-fork]
cd Resumos-e-Docs

# Criar branch
git checkout -b feature/novo-guia

# Fazer mudanças
git add .
git commit -m "Adiciona novo guia"

# Push
git push origin feature/novo-guia

# Criar Pull Request
```

### 2. **Padrões de Commit**
```
feat: adiciona novo guia de Kubernetes
fix: corrige bug na navegação
docs: atualiza documentação
style: melhora formatação do código
refactor: reorganiza estrutura de arquivos
```

## Recursos Úteis

### 1. **Documentação**
- [MDN Web Docs](https://developer.mozilla.org/)
- [CSS-Tricks](https://css-tricks.com/)
- [Can I Use](https://caniuse.com/)

### 2. **Ferramentas**
- [Figma](https://figma.com/) - Design
- [VS Code](https://code.visualstudio.com/) - Editor
- [GitHub](https://github.com/) - Versionamento
