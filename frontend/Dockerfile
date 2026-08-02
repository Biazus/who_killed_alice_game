# 1) Imagem base com Node
FROM node:20-alpine

# 2) Diretório de trabalho dentro do container
WORKDIR /app

# 3) Copiar apenas arquivos de dependências primeiro (melhor cache)
COPY package*.json ./

# 4) Instalar dependências
RUN npm install

# 5) Copiar o restante do código
COPY . .

# 6) Gerar build de produção do Vite (gera a pasta /dist)
RUN npm run build

# 7) Expor a porta que o Vite Preview vai usar
EXPOSE 4173

# 8) Rodar o servidor de preview do Vite servindo o build
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "4173"]