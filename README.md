# bunny-book-bot

Bot Telegram per gestire la libreria di manuali e file D&D di un gruppo. Il bot ha la personalità di **Vecchia Bunny**, un'anziana tartaruga (tortle) bibliotecaria appassionata di tisane e piante.

## Come funziona

- I manuali PDF vengono caricati **direttamente su Telegram** (dagli utenti, come normali allegati) in un topic dedicato di un gruppo forum — non passano mai per il filesystem del bot, quindi non c'è nessun limite di dimensione lato bot.
- Il bot resta in ascolto solo in quel topic: ogni volta che qualcuno carica un PDF lì, lo indicizza automaticamente (titolo dalla didascalia o dal nome del file) in un piccolo database SQLite, salvando solo il `file_id` Telegram del documento.
- Scrivendo `/lista` nel topic dei manuali (o in privato al bot), Vecchia Bunny risponde con l'elenco dei manuali disponibili come bottoni, accompagnato da una battuta in tema (tisane, piante, scaffali) diversa ogni volta.
- Cliccando un bottone, il bot invia il PDF **in privato** a chi lo ha richiesto (deve avere già avviato una chat privata con il bot almeno una volta) e poi ripulisce il topic cancellando sia il comando `/lista` sia la propria risposta con l'elenco.
- Fuori dal topic dei manuali (e fuori dalla chat privata), il bot ignora silenziosamente ogni comando, per non intasare gli altri topic del gruppo.

## Requisiti Telegram

Perché tutto funzioni servono alcune impostazioni sul bot/gruppo, fatte una tantum:

1. **Group Privacy disattivata** su BotFather (`/mybots` → il bot → *Bot Settings* → *Group Privacy* → *Turn off*), altrimenti il bot non vede i PDF caricati (vede solo i comandi). Se il bot era già nel gruppo prima di disattivarla, va rimosso e riaggiunto perché la modifica abbia effetto.
2. Il bot deve essere **amministratore del gruppo con il permesso "Elimina messaggi"**, altrimenti riesce a cancellare solo i propri messaggi e non il comando `/lista` di chi lo scrive.
3. Ogni utente che vuole ricevere manuali deve aver **scritto almeno un messaggio in privato al bot** una volta (requisito di Telegram: un bot non può scrivere per primo a un utente).

## Struttura del progetto

```
bunny_bot/
  config.py     # variabili d'ambiente (token, chat/topic id, percorso db)
  persona.py     # nome e battute di Vecchia Bunny
  catalog.py     # catalogo documenti su SQLite (titolo -> file_id Telegram)
  handlers.py    # /lista, indicizzazione upload, invio privato + pulizia topic
  main.py        # avvio dell'applicazione in long polling
systemd/
  bunny-bot.service  # unit file per l'avvio automatico al boot
```

## Configurazione

Copia `.env.example` in `.env` e compila:

```
BOT_TOKEN=           # token da @BotFather
GROUP_CHAT_ID=       # id del gruppo (numero negativo per i supergruppi)
MANUALI_TOPIC_ID=    # id del topic dove si caricano i manuali
CACHE_DB_PATH=data/catalog_cache.sqlite3
```

Per trovare `GROUP_CHAT_ID` e `MANUALI_TOPIC_ID`, basta far scrivere un messaggio nel topic e leggere `chat.id` / `message_thread_id` dalla risposta di `getUpdates` dell'API Telegram.

## Avvio

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m bunny_bot.main
```

## Avvio automatico (systemd)

```bash
sudo cp systemd/bunny-bot.service /etc/systemd/system/bunny-bot.service
sudo systemctl daemon-reload
sudo systemctl enable --now bunny-bot
journalctl -u bunny-bot -f
```

Il servizio riparte da solo ad ogni riavvio del sistema e in caso di crash (`Restart=on-failure`).
