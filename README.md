# Computer Security
 
O objetivo principal deste trabalho é o de construir uma plataforma para assinar e transmitir
ficheiros de um modo seguro, entre dois ou mais utilizadores, recorrendo apenas a mecanismos da criptografia simétrica e a um agente de confiança.

Entre outras, apontam-se as seguintes funcionalidades básicas do sistema a desenvolver:
 
• Deve ser possível fazer o registo junto do agente de confiança;

• O utilizador, depois de devidamente autenticado no sistema, deve poder escolher se
quer cifrar ou assinar um ficheiro antes de o enviar; deve também poder escolher o
utilizador para o qual quer enviar o ficheiro a partir de uma lista de utilizadores que se encontrem ligados ao sistema;

• Caso o utilizador escolha não cifrar o ficheiro a transmitir, este deve ser acompanhado
de um código de autenticação da mensagem (deve ser usado um Hash based Message Authentication Code (HMAC) para o efeito);

• As chaves de sessão devem ser geradas por um dos clientes e trocadas via agente de
confiança;

• O agente de confiança deve ser capaz de fazer assinaturas digitais de ficheiros transmitidos por utilizadores autenticados do sistema.

Note que a definição deste projeto indicia que o sistema só poderá estar completamente
operacional quando estão ligados, pelo menos, três intervenientes: (i) a aplicação (cliente)
que vai ser usada para transmitir o ficheiro, (ii) a aplicação (cliente) que vai ser usada
para receber o ficheiro e (iii), o agente de confiança. Pressupõe-se que o agente de
confiança já está a correr quando qualquer utilizador se tenta ligar ao sistema, que é este
que gera todas as chaves de sessão para confidencialidade nas comunicações, e que
alimenta cada cliente com as informações acerca de outros clientes ligados ao sistema
(para que determinado cliente possa enviar um ficheiro a outro, este deve estar online).
Pressupõe-se que as chaves de cifra de chaves de sessão são inseridas manualmente no
sistema aquando da inicialização de determinado cliente.

Podem fortalecer o trabalho e conhecimento através da implementação das seguintes funcionalidades:

• Permitir que apenas as primeiras chaves de cifra de chaves de sessão sejam trocadas
usando criptografia assimétrica.

• Garantir que as credenciais de autenticação no servidor / agente de confiança (i.e.
username e password) são trocadas de forma segura.

• Assegurar que as chaves de cifra de chaves de sessão mudam sempre que o utilizador
faz login no sistema, sem que se perca sincronismo e nunca recorrendo a mecanismos
de criptografia simétrica (pesquisar por one time password);

• Permitir que o utilizador escolha a cifra a utilizar e o comprimento da chave de cifra;

• Ter um help bastante completo.

Pensem numa forma de atacar o sistema (uma falha da sua implementação) e dediquem-lhe uma secção no relatório. Notem que, para efeitos de avaliação e prototipagem, o
sistema desenvolvido pode executar localmente todos os seus componentes/aplicações/programas, desde que simule ou concretize a arquitetura sugerida (i.e., não precisa necessariamente de executar em rede).
