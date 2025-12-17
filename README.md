# ABOUT:

This is a personal fragrance review tracker project for myself to learn the tools (some features still in development).
You can add any fragrance you own or tried with your score and it will get the public details about the fragrance.

Public information is pulled from Fragrantica and only for personal use.

Using:
- Polars for maintaining the database of fragrances
- NiceGUI for website generation
- curl-cffi for HTTP requests

# HOW TO USE:

Either run ./main.sh or the command inside it to start the server (Uvicorn). Planning to run this on a free hosting service for testing on other devices.

**WARNING: the import option for the database is not very reliable because the search results Algolia provides are pretty bad**

# TODOS

- Add more tests to facilitate easier updates and fix issues (e.g. changes in Fragrantica website)

- Add a field for personal note
- Add other fields like notes/accords/niche/season/sex
- Add display and search by score/notes
- Add similar fragrance suggestions (in your fragrances or online)
