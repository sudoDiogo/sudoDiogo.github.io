
const PROJECTS = [
  {
    id: "p01",
    title: "Preenchimento do formulário de diagnóstico inicial",
    tag: "Quiz/formulário",
    status: "Completo",
    tech: ["Google forms"],
    desc: "Resposta do primeiro formulário diagnóstico da disciplina",
    concepts: ["programação básica", "Introdução"],
    files: [
       { label: "print.png",       path: "arquivos/1confirmacao_resposta_quiz.png" }
    ]
  },
  {
    id: "p02",
    title: "QUIZ – Lógica de Programação",
    tag: "Formulário/quiz",
    status: "Completo",
    tech: ["Google forms"],
    desc: "Quiz sobre conhecimentos de programação",
    concepts: ["condicionais", "operadores lógicos"],
    files: [
      { label: "2.txt",       path: "arquivos/2.txt" }
    ]
  },
  {
    id: "p03",
    title: "QUIZ – Diagnóstico de Lógica de Programação",
    tag: "Quiz/formulário",
    status: "Completo",
    tech: ["Google forms"],
    desc: "Quiz diagnósitco sobre lógica de programação",
    concepts: ["laços de repetição", "lógica"],
    files: [
       { label: "3.txt",       path: "arquivos/3.txt" }
    ]
  },
  {
    id: "p04",
    title: "Lista de 15 exercícios: escolher e resolver",
    tag: "Lista",
    status: "Completo",
    tech: ["C"],
    desc: "Escolher e resolver 15 exercícios",
    concepts: ["condicionais", "retornos", "lógica"],
    files: [
      { label: "4.pdf",       path: "arquivos/4pdf.pdf" }
    ]
  },
  {
    id: "p05",
    title: "Lista de 10 Exercícios da INTRODUCAO A ALGORITMOS",
    tag: "Lista",
    status: "Completo",
    tech: ["Python"],
    desc: "Dez exercícios de introdução a Python",
    concepts: ["estrturas", "Python", "iteração"],
    files: [
      { label: "5.pdf",       path: "arquivos/5.pdf" }
    ]
  },
  {
    id: "p06",
    title: "Geração e Avaliação de Exercícios de Algoritmos com LLMs",
    tag: "Geração LLM",
    status: "Completo",
    tech: ["Claude AI", "Gemini", "Chat GPT"],
    desc: "Escrita e julgamento de algoritmos com LLM's",
    concepts: ["Engenharia de prompt", "Controle de LLM's"],
    files: [
      { label: "6.pdf",       path: "arquivos/6.pdf" }
    ]
  },
  {
    id: "p07",
    title: "Quiz de Avaliação da Atividade Anterior",
    tag: "Quiz/formulário",
    status: "Completo",
    tech: ["Google forms"],
    desc: "Quiz de opinião da atividade de geração de algoritmos.",
    concepts: ["avaliação", "LLM"],
    files: [
      { label: "7.txt",       path: "arquivos/7.txt" }
    ]
  },
  {
    id: "p08",
    title: "Resolver os 5 exercícios em papel",
    tag: "Lista/papel",
    status: "Completo",
    tech: ["Papel e caneta"],
    desc: "Resolver os pseudocódigos em papel e caneta..",
    concepts: ["lógica", "estrutura", "resolução de problemas"],
    files: [
      { label: "8pdf.pdf",       path: "arquivos/8pdf.pdf" }
    ]
  },
  {
    id: "p09",
    title: "Resolver os exercícios de listas/vetores/arrays em Python",
    tag: "Vetores Python",
    status: "Completo",
    tech: ["Python"],
    desc: "Lista de exercícios sobre vetores.",
    concepts: ["Listas", "arrays", "lógica"],
    files: [
      { label: "1vetor.py",       path: "arquivos/1vetor.py" },
      { label: "2vetor.py",       path: "arquivos/2vetor.py" },
      { label: "3vetor.py",       path: "arquivos/3vetor.py" },
      { label: "4vetor.py",       path: "arquivos/4vetor.py" },
      { label: "5vetor.py",       path: "arquivos/5vetor.py" },
      { label: "6vetor.py",       path: "arquivos/6vetor.py" },
      { label: "7vetor.py",       path: "arquivos/7vetor.py" },
      { label: "8vetor.py",       path: "arquivos/8vetor.py" },
      { label: "9vetor.py",       path: "arquivos/9vetor.py" },
      { label: "10vetor.py",       path: "arquivos/10vetor.py" },
      { label: "11vetor.py",       path: "arquivos/11vetor.py" },
      { label: "12vetor.py",       path: "arquivos/12vetor.py" },
      { label: "13vetor.py",       path: "arquivos/13vetor.py" },
      { label: "14vetor.py",       path: "arquivos/14vetor.py" },
      { label: "15vetor.py",       path: "arquivos/15vetor.py" }
    ]
  },
  {
    id: "p10",
    title: "Formulação e Resolução de Problemas com Vetores/Listas usando LLMs",
    tag: "Resolução com LLM",
    status: "Completo",
    tech: ["Claude AI"],
    desc: "Gerar exercícios com LLM e resolver.",
    concepts: ["engenharia de prompt", "organização", "pseudocódigo"],
    files: [
      { label: "10pdf.pdf",       path: "arquivos/10pdf.pdf" }
    ]
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
