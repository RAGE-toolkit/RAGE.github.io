import requests

def fetch_orcid_works(orcid_id):
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")
    data = response.json()
    works = data.get("group", [])
    publications = []
    for work in works:
        summary = work.get("work-summary", [])[0]

        title = summary.get("title", {}).get("title", {}).get("value", "No Title")
        
        # Handle potential NoneType for journal-title
        journal_info = summary.get("journal-title")
        journal = journal_info.get("value", "") if journal_info else ""

        # Handle potential NoneType for publication-date
        pub_date = summary.get("publication-date", {})
        year = pub_date.get("year", {}).get("value", "n.d.")

        external_ids = summary.get("external-ids", {}).get("external-id", [])
        doi = ""
        for eid in external_ids:
            if eid.get("external-id-type") == "doi":
                doi = eid.get("external-id-value")
                break
        link = f"https://doi.org/{doi}" if doi else ""

        publications.append({
            "title": title,
            "journal": journal,
            "year": year,
            "link": link
        })

    return publications


def generate_markdown(publications):
    md_lines = ["## 📚 Publications\n"]
    for pub in publications:
        line = f"- **{pub['title']}**"
        if pub['journal']:
            line += f", _{pub['journal']}_"
        line += f", {pub['year']}"
        if pub['link']:
            line += f" [DOI]({pub['link']})"
        md_lines.append(line)
    return "\n".join(md_lines)

if __name__ == "__main__":
    orcid_id = "0000-0001-9990-6299"  # Replace with your ORCID iD
    publications = fetch_orcid_works(orcid_id)
    markdown_content = generate_markdown(publications)
    with open("publications.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print("publications.md has been created.")
