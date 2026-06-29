
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
    title: "Gerar as diferentes versões do código até ter resultados visuais interessantes e consistentes",
    tag: "Geração de código",
    status: "Completo",
    tech: ["Python", "Claude AI"],
    desc: "Avaliação de códigos gerados por LLM",
    concepts: ["prompt", "python", "funções"],
    files: [
      { label: "v1.py",       path: "arquivos/v1.py" },
      { label: "v2.py",       path: "arquivos/v2.py" },
      { label: "v3.py",       path: "arquivos/v3.py" },
      { label: "v4.py",       path: "arquivos/v4.py" }
    ]
  },
  {
    id: "p12",
    title: "Problemas de outras disciplinas – resolução em múltiplas abordagens",
    tag: "Resolução de problemas",
    status: "Completo",
    tech: ["Python", "Lógica"],
    desc: "Resolver como múltiplas abordagens problemas de outras disciplinas que requerem lógica",
    concepts: ["pseudocódigo", "lógica", "programação"],
    files: [
      { label: "12pdf.pdf",       path: "arquivos/12pdf.pdf" }
    ]
  },
  {
    id: "p13",
    title: "Escolher e entregar 1 dos dois problemas de engenharia propostos",
    tag: "Resolução de problemas",
    status: "Completo",
    tech: ["Python", "Claude AI"],
    desc: "Escolher o problema a ser resolvido e utilizar uma LLM para gerar o código até estar bom.",
    concepts: ["controle de LLM", "organização", "lógica"],
    files: [
      { label: "13pdf.pdf",       path: "arquivos/13pdf.pdf" }
    ]
  },
  {
    id: "p14",
    title: "Entregar o outro dos dois problemas de engenharia propostos da aula passada",
    tag: "Resolução de problemas",
    status: "Completo",
    tech: ["Python", "Claude AI"],
    desc: "Escolher o outro problema e utilizar uma LLM para gerar outro código.",
    concepts: ["algoritmos", "engenharia de prompt"],
    files: [
       { label: "14pdf.pdf",       path: "arquivos/14pdf.pdf" }
    ]
  },
  {
    id: "p15",
    title: "Escolher e resolver um problema de engenharia",
    tag: "Resolução de problemas",
    status: "completp",
    tech: ["Python", "IDE"],
    desc: "Resolver um problema de engenharia utilizando LLM.",
    concepts: ["estruturas de dados", "lógica", "criatividade"],
    files: [
      { label: "medicina_tatica.py",       path: "arquivos/medicina_tatica.py" },
      { label: "MedicinaTática_DiogoFreitas_ET01.pdf",       path: "arquivos/MedicinaTática_DiogoFreitas_ET01.pdf" },
      { label: "planejamento_missao.png",       path: "arquivos/planejamento_missao.png" },
      { label: "home_software.png",       path: "arquivos/home_software.png" },
      { label: "aba_equipamentos.png",       path: "arquivos/aba_equipamentos.png" },
      { label: "equipamentos_filtrados.png",       path: "arquivos/equipamentos_filtrados.png" },
    ]
  },
  {
    id: "p16",
    title: "Evolução técnica da solução desenvolvida na atividade anterior",
    tag: "Evolução de código",
    status: "Completo",
    tech: ["Python", "Claude AI"],
    desc: "Melhorias da atividade anterior",
    concepts: ["funções", "bibliotecas", "recursividade"],
    files: [
      { label: "carregamento.png", path: "arquivos/carregamento.png" },
      { label: "drones3d.png", path: "arquivos/drones3d.png" },
      { label: "equipamentos.png", path: "arquivos/equipamentos.png" },
      { label: "home.png", path: "arquivos/home.png" },
      { label: "medicina_tatica.py", path: "arquivos/medicina_tatica.py" },
      { label: "melhoriasMedicinaTatica_DiogoET01.pdf", path: "arquivos/melhoriasMedicinaTatica_DiogoET01.pdf" },
      { label: "orbita.png", path: "arquivos/orbita.png" },
      { label: "planejamento_missao.png", path: "arquivos/planejamento_missao.png" },
      { label: "planejamento_missao2.png", path: "arquivos/planejamento_missao2.png" },
      { label: "situacao_atual.png", path: "arquivos/situacao_atual.png" }
    ]
  },
  {
    id: "p17",
    title: "Escreva um breve relato sincero sobre as entrevistas",
    tag: "Feedback de exercícios",
    status: "Completo",
    tech: ["Google meet"],
    desc: "Entrevista sobre exercícios de pseudocódigo",
    concepts: ["entrevista", "lógica"],
    files: [
      { label: "relato_entrevista.txt", path: "arquivos/relato_entrevista.txt"} 
    ]
  },
  {
    id: "p18",
    title: "Modularização de Código e Avaliação de LLMs",
    tag: "Resolução de problemas e modularização",
    status: "Completo",
    tech: ["Python", "Claude AI"],
    desc: "Desenvolvimento de uma  solução para um problema de monitoramento de grandezas de engenharia utilizando conceitos de modularização de código.",
    concepts: ["resolução de problemas", "programação", "prompt"],
    files: [
      { label: "claude_analisador_sinais.py", path: "arquivos/claude_analisador_sinais.py" },
      { label: "claude_gerador_medicoes.py", path: "arquivos/claude_gerador_medicoes.py" },
      { label: "claude_analisador_sinais.py", path: "arquivos/claude_analisador_sinais.py" },
      { label: "gpt_analisador_sinais.py", path: "arquivos/gpt_analisador_sinais.py" },
      { label: "gpt_gerador_medicoes.py", path: "arquivos/gpt_gerador_medicoes.py" },
      { label: "modularizacao_DiogoET01.pdf", path: "arquivos/modularizacao_DiogoET01.pdf"} 
    ]
  },

  {
    id: "p19",
    title: "Avaliar criticamente o site alegrete.org",
    tag: "Semana 18",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["banco de dados", "SQLite", "queries"],
    files: [
      { label: "avaliacao_alegrete.txt", path: "arquivos/avaliacao_alegrete.txt"} 
    ]
  },

  {
    id: "p20",
    title: "Desenvolvimento Assistido por IA para o Portal Alegrete.org",
    tag: "Semana 18",
    status: "em breve",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["banco de dados", "SQLite", "queries"],
    files: [
      { label: "GaleriaAlegretense_DiogoET01.pdf", path: "arquivos/GaleriaAlegretense_DiogoET01.pdf" },
      { label: "galeria_alegretense.py", path: "arquivos/galeria_alegretense.py" },
      { label: "categorias.py", path: "arquivos/categorias.py" },
      { label: "provedores.py", path: "arquivos/provedores.py" }
    ]
  },

  {
    id: "p21",
    title: "Postar o link e um print do seu site .github.io",
    tag: "Github.io",
    status: "Completo",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["banco de dados", "SQLite", "queries"],
    files: [
      { label: "print_inicial.png", path: "arquivos/print_inicial.png" },
      { label: "link.txt", path: "arquivos/link.txt" }
    ]
  },

  {
    id: "p22",
    title: "Projeto Final da Disciplina: Portfólio de Entregas no GitHub.io (Versão 1)",
    tag: "Github.io",
    status: "Completo",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["banco de dados", "SQLite", "queries"],
    files: [
      { label: "print_site.png", path: "arquivos/print_site.png" },
      { label: "link.txt", path: "arquivos/link.txt" }
    ]
  },

  {
    id: "p23",
    title: "Atividade em Aula: Portfólio no GitHub.io – Versão 26.03.2026",
    tag: "Github.io",
    status: "Completo",
    tech: ["Python"],
    desc: "Descrição breve do que foi desenvolvido neste projeto.",
    concepts: ["banco de dados", "SQLite", "queries"],
    files: [
      { label: "resumo26.06.2026.txt", path: "arquivos/resumo26.06.2026.txt" },
      { label: "link.txt", path: "arquivos/link.txt" }
    ]
  },
  
  {
    id: "p24",
    title: "Projeto Final",
    tag: "Projeto Final",
    status: "Completo",
    tech: ["Python", "Claude AI"],
    desc: "Projeto integrador do semestre, reunindo os conceitos trabalhados ao longo das aulas.",
    concepts: ["integração", "projeto completo", "boas práticas"],
    files: []
  }
];
