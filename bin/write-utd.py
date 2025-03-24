#!/usr/bin/env python3

# Verwerk UTD tot een documentatie in de vorm van een set Markdown-bestanden.

from rdflib import ConjunctiveGraph
from urllib.parse import quote, unquote
import time
import argparse
import os
import json

def main():
    args = parse_args()

    files = [
        f'{args["root"]}/ontology/def/utd/graaf-informatiemodel-utd.trig',
        f'{args["root"]}/ontology/def/utd/graaf-kennismodel-utd.trig',
        f'{args["root"]}/ontology/def/linksets/graaf-otl-utd-linkset.trig',

    ]

    print("Reading")
    print("...Initials")

    # Create an empty ConjunctiveGraph
    graph = ConjunctiveGraph()

    # Parse multiple .trig files into the graph

    for file in files:
        graph.parse(file, format="trig")

    print("Named Graphs in dataset:")
    for ctx in graph.contexts():
        print(ctx.identifier)
        
    # top_concepten_graaf_kennismodel = """
    # SELECT (COUNT(*) AS ?count) WHERE { 
    #     GRAPH <https://data.rws.nl/def/utd/graaf-kennismodel> { 
    #         ?s skos:prefLabel ?o .
    #         FILTER CONTAINS(STR(?o), " | - , - | - | -")
    #     }  
    # } LIMIT 50
    # """

    unieke_concepten_graaf_kennismodel = """
    SELECT ?resource ?label ?broader WHERE { 
        GRAPH <https://data.rws.nl/def/utd/graaf-kennismodel> { 
            ?resource a skos:Concept ;
                    skos:prefLabel ?label ;
                    skos:broaderTransitive ?broader .
        }  
    } ORDER BY ?label
    """

    utd_concepts = []

    for row in graph.query(unieke_concepten_graaf_kennismodel):
        utd_concepts.append({
            "resource": row["resource"],
            "label": row["label"],
            "broader": row["broader"],
        })

    with open(
        f'{args["root"]}/kernregister-catalogus/md-doc/utd-list.md', "w"
    ) as md_otl_list:
        md_otl_list.write("---\ntitle: UTD-concepten (alfabetisch)\nparent: RWS Kernregistraties\nnav_order: 1\n---\n")
        md_otl_list.write(
            "\n## Introductie\nDeze pagina bevat een overzicht van alle UTD-concepten."
        )

        table_head = """
            <tr>
                <th>Resource</th>
                <th>Broader Transitive</th>
            </tr>
        """

        for concept in utd_concepts:
            md_otl_list.write(f"<h2>{concept['label']}</h2>")
            
            md_otl_list.write("<table>")
            md_otl_list.write(table_head)
            md_otl_list.write(f"<tr><td>{concept['resource']}</td><td>{concept['broader']}</td></tr>")
            md_otl_list.write("</table>")


def parse_args():
    parser = argparse.ArgumentParser(description="Genereer documentatie voor de kernregistratie.")
    parser.add_argument(
        "root",
        help="Pad naar de root directory van de kernregistratie-repository. Indien niet gegeven wordt de huidige directory ('.') gebruikt.",
        nargs="?",
        default=os.getcwd(),
    )
    parser.add_argument(
        "-v", "--verbose", help="Geef extra output ter ondersteuning van ontwikkelen of debuggen.", action="store_true"
    )
    parser.add_argument(
        "-s", "--shortened", help="Gebruik een ingekort kennis- en informatiemodel.", action="store_true"
    )
    args = parser.parse_args()

    return {
        "root": args.root,
        "verbose": args.verbose,
        "shortened": args.shortened,
    }


if __name__ == "__main__":
    main()