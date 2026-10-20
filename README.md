# Soie & Or — soie-et-or.com

Statische website. De pagina's staan in `site/` en zijn gemaakt met `build.py` op basis van de teksten in `content.py`.

## Online zetten (Netlify + GitHub)

1. Maak een gratis GitHub-account en een nieuwe repository, bijvoorbeeld `soie-et-or`.
2. Upload de inhoud van deze map naar de repository (Add file > Upload files).
3. Maak een gratis Netlify-account, kies **Add new site > Import an existing project > GitHub** en selecteer de repository.
   Netlify leest `netlify.toml` en publiceert de map `site`.
4. In Netlify: **Domain management > Add a domain** en vul `www.soie-et-or.com` in. Volg de DNS-instructies bij je registrar.
5. Zet HTTPS aan (Netlify doet dit automatisch zodra het domein werkt).

## Nog invullen voor je je bij Awin aanmeldt

- `content.py` > `ABOUT`: vervang de tekst tussen [ ] door een korte persoonlijke noot.
- `content.py` > `PRIVACY`: vul je naam of bedrijfsnaam en woonplaats in.
- `content.py` > `SITE`: controleer de Pinterest-link en plak later de `p:domain_verify`-code van Pinterest.
- Zorg dat hello@soie-et-or.com werkt.

Na een wijziging: `python3 build.py` draaien, of laat Claude het doen.
