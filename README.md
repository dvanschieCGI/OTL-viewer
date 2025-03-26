# Deployment
Momenteel wordt de OTL-viewer gedoployed naar Github pages zodra er wordt gepusht naar de repo. Hier moet aan toegevoegd worden dat hij elke ochtend automatisch wordt gedeployed, zodat in het geval van een hack de OTL-viewer niet permanent uit de lucht is. Ook zal de viewer waarschijnlijk naar een Kubernetes cluster gemigreerd worden.
## Aanpak
### Dagelijkse deployment
De dagelijkse deployment kan geautomatiseerd worden aan de hand van een cronjob. Dit kan gedaan worden door een schedule toe te voegen aan het on argument van de `build-and-demploy.yml` workflow:
```yaml
on:
    push:
        branches: ["main"]

    schedule:
    - cron: '0 6 * * *'
```
Deze cronjob zal elke dag om 6:00 de workflow triggeren.
### Kubernetes
Om te deployen naar een kubernetes cluster
https://github.com/Azure/k8s-deploy


# Mapping file
De mappingfile wordt bij elke deployment gegenereerd op basis van de csv bestanden op de airbim-mappingrule-generator repo. De CSV bestanden die gebruikt worden als bron zijn hier te vinden: https://github.com/RWS-NL/airbim-mappingrule-generator/tree/master/mappingregels 

# Gebruikte Technologieën 
De OTL viewer maakt gebruik van een aantal technologieën. De licenties van deze technologieën zijn hieronder inzichtelijk gemaakt.

| Technologie | Licentie | Activiteit |
|-------------|----------|------------|
| RDFLib | [BSD 3-Clause](https://github.com/RDFLib/rdflib/blob/main/LICENSE) | Actief onderhouden, redelijk actieve Github issues |
| Jekyll | [MIT](https://github.com/jekyll/jekyll/blob/master/LICENSE) | Actief onderhouden, grote community |
| jekyll-toc | [MIT](https://github.com/jekyll/jekyll/blob/master/LICENSE) | Laatste update 10 maanden geleden, maar het is een lichtgewicht plugin voor genereren van table of content|
| Just the Docs | [MIT](https://github.com/just-the-docs/just-the-docs/blob/main/LICENSE.txt) | Actief onderhouden en activiteit in Github issues |
