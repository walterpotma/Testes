# 🚀 Guia de Deploy

## Opções de Deploy

### 1. **Desenvolvimento Local**
```bash
# Usando Python
cd public
python -m http.server 8000

# Usando Node.js
npx live-server public

# Usando PHP
cd public
php -S localhost:8000
```

### 2. **Produção com Docker**
```bash
# Build da imagem
docker build -t resumos-docs .

# Executar container
docker run -p 80:80 resumos-docs

# Com docker-compose
docker-compose up -d
```

### 3. **Produção com Nginx**
```bash
# Copiar arquivos
sudo cp -r public/* /var/www/html/

# Configurar Nginx
sudo cp nginx.conf /etc/nginx/nginx.conf
sudo nginx -t
sudo systemctl reload nginx
```

## Configuração do Docker

### Dockerfile
```dockerfile
FROM nginx:alpine

# Copiar arquivos estáticos
COPY public/ /usr/share/nginx/html/

# Copiar configuração do Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Expor porta 80
EXPOSE 80

# Comando padrão
CMD ["nginx", "-g", "daemon off;"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  resumos-docs:
    build: .
    ports:
      - "80:80"
    restart: unless-stopped
    volumes:
      - ./public:/usr/share/nginx/html:ro
    environment:
      - NGINX_HOST=localhost
      - NGINX_PORT=80
```

## Configuração do Nginx

### Configuração Básica
```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;
    
    # Compressão
    gzip on;
    gzip_types text/css application/javascript;
    
    # Cache
    location ~* \.(css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Configuração Avançada
```nginx
# Segurança
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";

# Performance
sendfile on;
tcp_nopush on;
tcp_nodelay on;
```

## Deploy em Diferentes Ambientes

### 1. **Desenvolvimento**
```bash
# Servidor local
cd public
python -m http.server 8000
```

### 2. **Staging**
```bash
# Docker
docker build -t resumos-docs:staging .
docker run -p 8080:80 resumos-docs:staging
```

### 3. **Produção**
```bash
# Docker
docker build -t resumos-docs:latest .
docker run -d -p 80:80 --name resumos-docs resumos-docs:latest

# Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Monitoramento

### 1. **Health Check**
```bash
# Verificar se está funcionando
curl http://localhost/health

# Verificar logs
docker logs resumos-docs
sudo journalctl -u nginx
```

### 2. **Métricas**
```bash
# CPU e Memória
docker stats resumos-docs

# Logs de acesso
sudo tail -f /var/log/nginx/access.log
```

## SSL/HTTPS

### 1. **Let's Encrypt**
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com

# Renovação automática
sudo crontab -e
# Adicionar: 0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. **Configuração HTTPS**
```nginx
server {
    listen 443 ssl http2;
    server_name seu-dominio.com;
    
    ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;
    
    # Configurações SSL
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

## CI/CD

### 1. **GitHub Actions**
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Build Docker image
      run: docker build -t resumos-docs .
    
    - name: Deploy to server
      run: |
        docker save resumos-docs | ssh user@server docker load
        ssh user@server docker run -d -p 80:80 resumos-docs
```

### 2. **GitLab CI**
```yaml
stages:
  - build
  - deploy

build:
  stage: build
  script:
    - docker build -t resumos-docs .
    - docker push registry.gitlab.com/user/resumos-docs

deploy:
  stage: deploy
  script:
    - docker pull registry.gitlab.com/user/resumos-docs
    - docker run -d -p 80:80 registry.gitlab.com/user/resumos-docs
```

## Backup e Recuperação

### 1. **Backup dos Arquivos**
```bash
# Backup completo
tar -czf backup-$(date +%Y%m%d).tar.gz public/ nginx.conf

# Backup incremental
rsync -av --link-dest=/backup/last public/ /backup/$(date +%Y%m%d)/
```

### 2. **Recuperação**
```bash
# Restaurar backup
tar -xzf backup-20231201.tar.gz

# Restaurar com rsync
rsync -av /backup/20231201/ public/
```

## Troubleshooting

### 1. **Problemas Comuns**
```bash
# Nginx não inicia
sudo nginx -t
sudo systemctl status nginx

# Docker não inicia
docker logs resumos-docs
docker ps -a

# Permissões
sudo chown -R www-data:www-data /var/www/html/
```

### 2. **Logs**
```bash
# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Docker logs
docker logs -f resumos-docs
```

## Performance

### 1. **Otimizações**
- Compressão Gzip
- Cache de arquivos estáticos
- Minificação de CSS/JS
- Otimização de imagens

### 2. **Monitoramento**
```bash
# Lighthouse
npx lighthouse http://localhost --view

# PageSpeed Insights
# https://pagespeed.web.dev/
```

## Segurança

### 1. **Headers de Segurança**
```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-Content-Type-Options "nosniff";
add_header X-XSS-Protection "1; mode=block";
add_header Referrer-Policy "no-referrer-when-downgrade";
```

### 2. **Firewall**
```bash
# UFW (Ubuntu)
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```
