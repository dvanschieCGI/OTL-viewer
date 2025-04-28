#!/usr/bin/env python3

# Verwerk UTD tot een documentatie in de vorm van een set Markdown-bestanden.

from rdflib import ConjunctiveGraph, RDF
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


    # Add "heeftElement" to the UTD concepts
    utd_heeft_element_query = """
    SELECT ?resource ?heeftElement
    WHERE {
        GRAPH <https://data.rws.nl/def/utd/graaf-kennismodel> {  
            ?resource utd:heeftElement ?heeftElement .
        }
    }
    ORDER BY ?resource
    """

    for row in graph.query(utd_heeft_element_query):
        resource = row["resource"]
        element = row["heeftElement"]

        for utd_concept in utd_concepts:
            if utd_concept["resource"] == resource:
                utd_concept.setdefault("hasParts", []).append(element)
                break

    # Add "heeftEenElement" to the UTD concepts
    utd_heeft_een_element_query = """
    SELECT ?resource ?heeftEenElement
    WHERE {
        GRAPH <https://data.rws.nl/def/utd/graaf-kennismodel> {
            ?resource utd:heeftEenElement ?heeftEenElement .
        }
    }
    ORDER BY ?resource
    """

    for row in graph.query(utd_heeft_een_element_query):
        resource = row["resource"]
        element = row["heeftEenElement"]

        # walk trough heeftEenElement (a BlindNode) to extract all present elements
        current = element
        while current and current != RDF.nil:
            first = graph.value(subject=current, predicate=RDF.first)
            if first:
                for utd_concept in utd_concepts:
                    if utd_concept["resource"] == resource:
                        utd_concept.setdefault("hasParts", []).append(first)
                        break
            current = graph.value(subject=current, predicate=RDF.rest)

    with open(
        f'{args["root"]}/kernregister-catalogus/md-doc/utd-list.md', "w"
    ) as md_otl_list:
        md_otl_list.write("---\ntitle: UTD-concepten (alfabetisch)\nparent: RWS Kernregistraties\nnav_order: 1\n---\n")
        md_otl_list.write(
            "\n## Introductie\nDeze pagina bevat een overzicht van alle UTD-concepten."
        )

        table_head = "<tr> \n <th>Item</th> \n <th>Waarde</th> \n </tr>\n"

        for concept in utd_concepts:
            md_otl_list.write(f"\n<h2>{concept['label']}</h2>\n")
            
            md_otl_list.write("<table>\n")
            md_otl_list.write(table_head)
            md_otl_list.write(f"<tr>\n<td>Resource</td>\n<td>{concept['resource']}</td>\n</tr>\n")
            md_otl_list.write(f"<tr>\n<td>Broader Transitive</td>\n<td>{concept['broader']}</td>\n</tr>\n")
            md_otl_list.write("</table>")

            md_otl_list.write("<table>\n")
            md_otl_list.write("<tr> \n <th>Item</th> \n </tr>\n")
            # write hasParts to the table
            if "hasParts" in concept:
                for hasPart in concept["hasParts"]:
                    md_otl_list.write(f"<tr>\n<td>{hasPart}</td>\n</tr>\n")

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