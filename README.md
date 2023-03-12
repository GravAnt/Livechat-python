# Sistema di file sharing P2P 
Il sistema realizzato è un software di messaggistica e file sharing tra nodi utilizzando il modello P2P ibrido, in 
cui è presente un discovery server. È stato scelto questo modello perché è più vantaggioso rispetto al P2P 
strutturato e non strutturato. Infatti, il discovery server si occuperà non solo di permettere ai nodi di vedersi, 
ma anche di gestire un sistema di accounting. Infatti, ogni utente dovrà registrarsi per poter utilizzare il servizio, 
per cui la presenza del discovery server è utile per la creazione di nuovi account e per l’autenticazione. <br>
Le credenziali sono salvate in un database (il DBMS utilizzato è PostgreSQL) e la password è criptata (mediante 
Bcrypt). Il server gestisce anche un sistema di report di utenti, in modo da poter “bannare” un profilo nel caso 
in cui abbia ricevuto delle segnalazioni da parte di altri utenti. 
La comunicazione tra i nodi avviene in P2P. <br>

Per la realizzazione di un software di messaggistica e file sharing P2P sono stati utilizzati i seguenti strumenti:
<li>Linguaggio di programmazione: Python versione 3.11.1</li>
<li>IDE: Visual Studio Code versione 1.74</li>
<li>DBMS: PostgreSQL 14</li>
<li>Piattaforma di Version Control: GitHub</li>
<li>Sistema Operativo: Windows 10</li>
<br>
Il sistema realizzato è un progetto presentato per il corso di Reti di calcolatori del CdL Informatica e Comunicazione Digitale (Università degli studi di Bari).
