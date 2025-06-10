# MiniLang - Mini Linguagem de Programação

## Trabalho Prático Integrado: "Construindo sua Mini Linguagem de Programação"

## Instalação e Uso

### Pré-requisitos

```bash
pip install ply
```

### Como usar

**Modo Interativo (REPL):**

```bash
python minilang.py
```

**Executar arquivo:**

```bash
python minilang.py exemplo.ml
```

### Exemplos de Uso no REPL

```python
>>> 4 + 6
10
>>> x = 5
>>> x * 2
10
>>> print("Hello World")
Hello World
```

### 1. Objetivos e Público da Linguagem (Capítulos 1-3)

**Objetivo:** MiniLang é uma linguagem de programação educacional projetada para ensinar conceitos fundamentais de programação de forma simples e intuitiva.

**Público-alvo:**

- Estudantes iniciantes em programação
- Pessoas que querem entender como linguagens funcionam internamente
- Educadores que precisam de uma ferramenta simples para ensino

**Características principais:**

- Sintaxe simples e limpa
- Tipos de dados básicos (int, float, string, list, bool)
- Estruturas de controle essenciais
- Suporte a funções
- Interpretador interativo (REPL)

### 2. Análise Léxica e Sintática (Capítulo 4)

O interpretador utiliza PLY (Python Lex-Yacc) para implementar:

**Análise Léxica (Lexer):**

- Reconhece tokens como números, strings, identificadores, operadores
- Ignora espaços e comentários (iniciados com #)
- Trata palavras reservadas

**Análise Sintática (Parser):**

- Gramática definida em formato BNF
- Precedência de operadores configurada
- Tratamento de erros sintáticos

### 3. Nomes, Vinculações e Escopos (Capítulo 5)

**Implementação de Escopos:**

```python
# Escopo global
x = 10

def teste():
    # Escopo local da função
    y = 20
    return x + y  # Acessa variável global

resultado = teste()  # resultado = 30
```

**Características:**

- Escopo global para variáveis e funções principais
- Escopo local para parâmetros e variáveis dentro de funções
- Busca hierárquica: local → global
- Closures: funções "lembram" do ambiente onde foram definidas

### 4. Tipos de Dados (Capítulo 6)

**Tipos Suportados:**

```python
# Inteiros
idade = 25

# Floats
altura = 1.75

# Strings
nome = "João"

# Listas
numeros = [1, 2, 3, 4, 5]
mista = [1, "texto", 3.14, True]

# Booleanos
ativo = True
inativo = False
```

**Operações por Tipo:**

- Números: aritméticas (+, -, *, /, %)
- Strings: concatenação (+)
- Listas: concatenação (+), acesso por índice
- Booleanos: operações lógicas (and, or, not)

### 5. Atribuições (Capítulo 7)

**Tipos de Atribuição:**

```python
# Atribuição simples
x = 10

# Atribuições compostas
x += 5   # x = x + 5
x -= 2   # x = x - 2
x *= 3   # x = x * 3
x /= 2   # x = x / 2
```

### 6. Controle de Fluxo (Capítulo 8)

**Estrutura Condicional:**

```python
if idade >= 18:
    print("Maior de idade")
else:
    print("Menor de idade")
```

**Laço While:**

```python
contador = 0
while contador < 5:
    print(contador)
    contador += 1
```

**Laço For:**

```python
# Iteração sobre lista
for numero in [1, 2, 3, 4, 5]:
    print(numero)

# Iteração sobre string
for char in "Hello":
    print(char)
```

### 7. Subprogramas (Capítulos 9 e 10)

**Definição de Funções:**

```python
# Função simples
def saudacao():
    print("Olá, mundo!")

# Função com parâmetros
def soma(a, b):
    return a + b

# Função com múltiplos parâmetros
def calcular_media(lista):
    total = 0
    for num in lista:
        total += num
    return total / len(lista)
```

**Chamada de Funções:**

```python
saudacao()                    # Olá, mundo!
resultado = soma(5, 3)        # resultado = 8
media = calcular_media([1, 2, 3, 4, 5])  # media = 3.0
```

## Exemplos Completos

### Exemplo 1: Calculadora Simples

```python
def calculadora(a, b, operacao):
    if operacao == "+":
        return a + b
    else:
        if operacao == "-":
            return a - b
        else:
            if operacao == "*":
                return a * b
            else:
                if operacao == "/":
                    if b != 0:
                        return a / b
                    else:
                        return "Erro: divisão por zero"

print(calculadora(10, 5, "+"))  # 15
print(calculadora(10, 5, "/"))  # 2.0
```

### Exemplo 2: Lista de Números Pares

```python
def numeros_pares(limite):
    pares = []
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        if i <= limite:
            if i % 2 == 0:
                pares += [i]  # Adiciona à lista
    return pares

resultado = numeros_pares(8)
print(resultado)  # [2, 4, 6, 8]
```

### Exemplo 3: Fatorial

```python
def fatorial(n):
    if n <= 1:
        return 1
    else:
        resultado = 1
        contador = 2
        while contador <= n:
            resultado *= contador
            contador += 1
        return resultado

print(fatorial(5))  # 120
```

### Exemplo 4: Números Primos

```python
def eh_primo(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def listar_primos(limite):
    primos = []
    i = 2
    while i <= limite:
        if eh_primo(i):
            primos += [i]
        i += 1
    return primos

primos = listar_primos(20)
print(primos)  # [2, 3, 5, 7, 11, 13, 17, 19]
```

## Arquitetura do Interpretador

### Componentes Principais

1. **MiniLangLexer**: Análise léxica
   - Tokenização do código fonte
   - Reconhecimento de palavras reservadas
   - Tratamento de literais e identificadores

2. **MiniLangParser**: Análise sintática e semântica
   - Parser descendente recursivo
   - Construção da AST implícita
   - Execução direta durante o parsing

3. **Environment**: Gerenciamento de escopo
   - Encadeamento de ambientes
   - Resolução de nomes
   - Armazenamento de variáveis e funções

4. **Function**: Representação de funções
   - Parâmetros e corpo da função
   - Closure (captura do ambiente)

### Fluxo de Execução

1. **Tokenização**: Código fonte → Tokens
2. **Parsing**: Tokens → AST + Execução
3. **Avaliação**: Execução das operações
4. **Gerenciamento de Ambiente**: Resolução de variáveis

## Limitações e Extensões Futuras

### Limitações Atuais

- Sem arrays associativos/dicionários
- Sem tratamento de exceções
- Sem importação de módulos
- Sem classes/objetos
- Sem operações de E/S de arquivo

### Possíveis Extensões

- Adicionar mais tipos de dados
- Implementar sistema de módulos
- Adicionar programação orientada a objetos
- Melhorar mensagens de erro
- Adicionar debugger
- Compilação para bytecode

## Conclusão

MiniLang demonstra com sucesso os conceitos fundamentais de linguagens de programação, incluindo análise léxica e sintática, gerenciamento de tipos, escopos, controle de fluxo e subprogramas. O interpretador serve como base sólida para entender como linguagens mais complexas funcionam internamente.
