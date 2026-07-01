# TVlive

Playlist IPTV italiana personale, generata automaticamente da una sorgente M3U e ottimizzata per Kodi + IPTV Simple Client.

## URL playlist

https://raw.githubusercontent.com/Patroz1/TVlive/main/playlist/live-it.m3u

## Caratteristiche

- Playlist M3U italiana ordinata per gruppi e numerazione LCN
- Loghi canale tramite URL raw GitHub
- Compatibile con Kodi / IPTV Simple Client
- Canali Discovery delegati a WLTV Helper
- Pipeline di build automatica
- Catalogo canali in formato JSON

## Canali Discovery via WLTV

- NOVE
- Real Time
- DMAX
- Discovery Channel
- Giallo
- Food Network
- HGTV
- Discovery Turbo

## Uso su Kodi

Impostare IPTV Simple Client con URL remoto:

https://raw.githubusercontent.com/Patroz1/TVlive/main/playlist/live-it.m3u

## Build locale

python3 build.py

## Aggiornamento repository

python3 build.py
git add .
git commit -m "Update playlist"
git push