const PROJECTS = [
  {
    id: "p01",
    title: "Preenchimento do formulário de diagnóstico inicial",
    tag: "Formulário/quiz",
    status: "Completo",
    tech: ["Google forms"],
    desc: "Primeiro quiz",
    concepts: [],
    files: [
       { label: "confirmacao_resposta.png",    path: "arquivos/1confirmacao_resposta_quiz.png" },

    ]
  },
  {
    id: "p02",
    title: "Quiz de lógica de programação",
    tag: "Formulário/quiz",
    status: "Completo",
    tech: ["Google forms"],
    desc: "Quiz para avaliar lógica de programação",
    concepts: ["condicionais", "operadores lógicos", "programação"],
    files: []
  },
  {
    id: "p03",
    title: "Diagnóstico de lógica de programação",
    tag: "Formulário/quiz",
    status: "Completo",
    tech: ["Google forms"],
    desc: "Avaliação diagnóstica do quiz anterior sobre lógica de programação.",
    concepts: ["laços de repetição", "while", "for"],
    files: []
  },
  {
    id: "p04",
    title: "Lista de 15 exercícios: escolher e resolver",
    tag: "Programação",
    status: "Completo",
    tech: ["C"],
    desc: "Exercícios resolvidos em C.",
    concepts: ["condicionais", "programação introdutória"],
    files: [
          { label: "4pdf.pdf",    path: "arquivos/4pdf.pdf" }
      
    ]
  },
  {
    id: "p05",
    title: "Lista de 10 Exercícios da INTRODUCAO A ALGORITMOS com Python",
    tag: "Lista de programação",
    status: "Completo",
    tech: ["Python"],
    desc: "Lista de exercícios de introdução resolvidos em python.",
    concepts: ["introdução ao python"],
    files: []
  },
  {
    id: "p06",
    title: "Geração e Avaliação de Exercícios de Algoritmos com LLMs",
    tag: "Geração com LLM",
    status: "Completo",
    tech: ["Claude AI", "Gemini", "Chat GPT"],
    desc: "Geração de exercícios de programação criados por LLM's.",
    concepts: ["engenharia de prompt", "Controle de LLM's"],
    files: []
  },
  {
    id: "p07",
    title: "Quiz de Avaliação da Atividade: Uso de LLMs em Algoritmos e Programação",
    tag: "Formulário/quiz",
    status: "Completo",
    tech: ["Google forms"],
    desc: "Avaliação da atividade anterior com LLM's",
    concepts: ["Diagnóstico"],
    files: []
  },
  {
    id: "p08",
    title: "Resolver os 5 exercícios em papel",
    tag: "Programar no papel",
    status: "Completo",
    tech: ["Papel"],
    desc: "Escrita de pseudocódigos no papel",
    concepts: ["criatividade", "lógica"],
    files: []
  },
  {
    id: "p09",
    title: "Projeto 09",
    tag: "Semana 09",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["exceções", "try/except", "erros"],
    files: []
  },
  {
    id: "p10",
    title: "Projeto 10",
    tag: "Semana 10",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["módulos", "importação", "bibliotecas padrão"],
    files: []
  },
  {
    id: "p11",
    title: "Projeto 11",
    tag: "Semana 11",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["OOP", "classes", "objetos"],
    files: []
  },
  {
    id: "p12",
    title: "Projeto 12",
    tag: "Semana 12",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["herança", "polimorfismo", "encapsulamento"],
    files: []
  },
  {
    id: "p13",
    title: "Projeto 13",
    tag: "Semana 13",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["recursão", "pilha de chamadas"],
    files: []
  },
  {
    id: "p14",
    title: "Projeto 14",
    tag: "Semana 14",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["algoritmos de busca", "ordenação"],
    files: []
  },
  {
    id: "p15",
    title: "Projeto 15",
    tag: "Semana 15",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["estruturas de dados", "pilha", "fila"],
    files: []
  },
  {
    id: "p16",
    title: "Projeto 16",
    tag: "Semana 16",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["expressões regulares", "regex"],
    files: []
  },
  {
    id: "p17",
    title: "Projeto 17",
    tag: "Semana 17",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["APIs", "requests", "JSON"],
    files: []
  },
  {
    id: "p18",
    title: "Projeto 18",
    tag: "Semana 18",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["banco de dados", "SQLite", "queries"],
    files: []
  },
  {
    id: "p19",
    title: "Projeto Final",
    tag: "Projeto Final",
    status: "em breve",
    tech: ["Python", "Claude AI"],
    desc: "Projeto integrador do semestre, reunindo os conceitos trabalhados ao longo das aulas.",
    concepts: ["integração", "projeto completo", "boas práticas"],
    files: []
  }
];
