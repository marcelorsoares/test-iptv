**IPTV LIST GENERATE/TEST**

Aplicação para importar uma ou mais lista de IPTV, organizar e gerar uma lista com os canais, removendo os canais que não estão funcionando corretamente.

**Instalação:**

- Crie um arquivo settings.py dentro da pasta iptv;
- Execute o comando **python manage.py importar_canais _{NOME-DO-ARQUIVO} {True/False}_**, aonde _**{NOME-DO-ARQUIVO}**_ é o nome do arquivo da lista que você deseja importar, estando dentro da pasta importar e use __True__ ou __False__ para indicar se deseja testar se o stream está funcionando corretamente.
- Para gerar uma lista com todos os canais rode a aplicação e acesse a url **/lista.m3u**