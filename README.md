# ABOUT:

This is a personal fragrance review tracker project for myself to learn the tools (some features still in development).
You can add any fragrance you own or tried with your score and it will get the public details about the fragrance.

Public information is pulled from Fragrantica and only for personal use. Only getting a few links and downloading the card image directly, need to look for options on reducing the traffic even more (you will get locked out of the page if you decide to update images from every fragrance you tried).

Using Polars for maintaining the database of fragrances, NiceGUI for website generation. The website is very generic with only basic functionality, need to play around NiceGUI more.

# HOW TO USE:

Either run ./main.sh or the command inside it to start the server (Uvicorn). Planning to run this on a free hosting service for testing on other devices.

**WARNING: the import option for the database is not very reliable because the search results Algolia provides are pretty bad**

P.S. all functionality is there, but there are still a lot of optimisation to be done, also missing a lot of tests

# TODOS

- Add more tests to facilitate easier updates and fix issues (e.g. changes in Fragrantica website)

- Add a field for personal note
- Add other fields like notes/accords/niche/season/sex
- Add display and search by score/notes
- Add similar fragrance suggestions (in your fragrances or online)
