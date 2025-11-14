<h1 align="center">Software de Organização STP</h1>


Esse é um programa feito para testar a adaptação da equipe a um sistema de padronização e automatização. Nós desenvolvemos o SOSTP para superar a lacuna comunicativa entre as equipes de suporte imediato e de tecnicos de campo, pois um das dificuldades relatadas mais presentes nas pesquisas com colaboradores da STP foi que não havia um padrão nas requisições feitas à equipe técnica pela equipe de atendimento primário. Nesse sentido o SOSPT estabelece uma forma única de fazer essas requisições.
Abaixo o link para um vídeo demonstrativo sobre o funcionamento do SOSTP:

<p align='center' style="font-size: 15px"><b>Demo do SOSTP:</b></p>
<div align="center">
  <a href="https://www.youtube.com/watch?v=rbA1JpR1piQ">
    <img src="https://br.pinterest.com/pin/1059753356081479474/" width="600" />
  </a>
</div>
<p align='center' style="font-size: 10px">Clique para ver o conteúdo completo.</p>

O programa foi instalado nas máquinas da equipe de atendimento, a partir daí ele permite ao atendente gerar requisições iniciais e em mais dois níveis de gravidade.
Inicialmente ao atender o cliente o tecnico de triagem realiza o primeiro contato e a primeira tentativa de resolução do problema realizando verificações padrão, que devem ser feita afim de evitar que casos simples se tornem situações de campo ao passar problemas rudimentares para n1. Mas se o problema não puder ser resolvido na triagem, o atendente deve preencher um relatório padronizado com informações específicas detalhando a situação com as respostas obtidas. Abaixo uma ilustração do modelo de ficha da triagem:
<br>

<p align='center' style="font-size: 15px"><b>Ficha de triagem</b></p>
<div align="center">
  <a href="https://www.youtube.com/watch?v=0YLoEgbq0yo">
    <img align="center" src = "Pictures\Captura de tela 2025-11-12 162605.png" width = 400>
  </a>
</div>

<br>
<br>
Quando falamos de um problema de nível 1, já estamos tratando de um tralho de campo, nesse nível o técnico realiza o deslocamento afim de resolver a situação relatada pelo tecnico da triagem. No local ele realiza testes e verifica a condição e integridade dos equipamentos tanto no equipamento principal quanto no sistema de alimentação. Assim ele verifica a situação dos cabos, se estão gastos, apresentam cortes ou se seu comprimento se encontra fora do limite técnico. Normalmente, nessa etapa o técnico localiza e resolve o problema, contudo, caso a complicação ainda persista, ele deve finalizar relatando o diagnóstico e o tempo empreendido na tentativa de resolução, e então encaminha o problema para o nível 2 junto das informações necessárias. A seguir uma ilustração do relatório n1 para n2.
<br>
<br>

<p align='center' style="font-size: 15px"><b>Ficha N1</b></p>
<div align="center">
  <a href="https://www.youtube.com/watch?v=0YLoEgbq0yo">
    <img align="center" src = "Pictures\Captura de tela 2025-11-12 162623.png" width = 400>
  </a>
</div>

<br>
<br>
Após o nível 1 garantir a integridade da camada física, o técnico de nível 2 passa a atuar no nível lógico e de software, verificando configurações de rede, acesso, integração com outros sistemas e demais ajustes necessários. O técnico finaliza relatando se o problema foi ou não resolvido. Abaixo está a ilustração da ficha n2:
<br>
<br>

<p align='center' style="font-size: 15px"><b>Ficha N2</b></p>
<div align="center">
  <a href="https://www.youtube.com/watch?v=0YLoEgbq0yo">
    <img align="center" src = "Pictures\Captura de tela 2025-11-12 162645.png" width = 400>
  </a>
</div>

<br>
<br>

Ao final das etapas de triagem ou nível 1, caso o técnico tenha solucionado o problema, o atendimento deve ser encerrado, registrando a resolução da falha. Caso contrário, o técnico deve acionar a opção “Gerar Relatório”, função que baixa automaticamente o formulário preenchido e o envia para o e-mail do próximo nível de atendimento.
Dessa forma, garantimos que todas as requisições sigam um padrão único, ágil e autônomo. A integração desse sistema com o processo de treinamento dos técnicos de triagem evita que problemas simples se tornem ocorrências de campo, reduzindo a necessidade de deslocamento e prevenindo a sobrecarga das equipes de nível 1 e nível 2.

### ⚙️ Tecnologias Utilizadas 

Linguagens, ferramentas e bibliotecas utilizadas no desenvolvimento do projeto:

* [Python](https://www.python.org/)
* [Google Forms](https://docs.google.com/forms/u/0/)
* [Python's lib: email](https://docs.python.org/3/library/email.html)
* [PyInstaller](https://pyinstaller.org/en/stable/)
* [HTML](https://www.w3.org/html/)
* [CSS](https://www.w3.org/Style/CSS/Overview.en.html)

## ⚠️ Problemas enfrentados

### Excesso de etapas manuais:
No início, o programa funcionava de forma manual, usando apenas requisições HTML. O técnico de triagem precisava ter o relatório em seu computador para caso tenha que realatar e passar o problema a outro nível, tendo ainda que enviar esse relatório manualmente para o gmail do suporte de próximo nível.
* **Como solucionar:** Aplicamos técnicas de automação, usando uma linguagem de programação robusta. Criamos um programa usando Python para que ele mesmo ficasse encarregado de abrir a página de formulários e de acordo com a decisão do técnico, ele anexa automaticamente esse formulário no corpo de um e-mail e envia esse e-mail para o próximo nível de suporte.

### Erro de ambiente:
Nós precisavamos executar o programa em máquinas diferentes, e um problema comum quando se exporta um programa para outro ambiente é que isso pode gerar uma série de imcompatibilidades, como erros devido a caminhos diferentes no ambiente, ausência de componentes fundamentais para o funcionamento ou componentes em versões que não se correspondem.
* **Como solucionar:** Uma dos motivos de termos decidido usar uma linguagem de programação, é que assim existe a possibilidade de empacotar todos os componentes necessários para o funcionamento em um arquivo executável. Nós usamos a biblioteca de instalações do Python, o Pyinstaller, assim nós desenvolmemos um programa que funcionava em ambientes diversos.

## ⏭️ Próximos passos
Os testes se mostraram promissores, e por essa razão a STP decidiu prosseguir com a ideia, mas com uma versão profissional, por questões de segurança, escalabilidade e maior integração com seus sistemas.
