import os

import pandas as pd
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Talent Vault",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.title("Talent Vault")


@st.cache_data(ttl=5)
def fetch_stats() -> dict:
    response = requests.get(f"{API_BASE}/stats", timeout=5)
    response.raise_for_status()
    return response.json()


def fetch_persons(city: str, company: str, search: str, limit: int, offset: int) -> dict:
    params = {"limit": limit, "offset": offset}
    if city:
        params["city"] = city
    if company:
        params["company"] = company
    if search:
        params["search"] = search
    response = requests.get(f"{API_BASE}/persons", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_person(passport: str) -> dict | None:
    response = requests.get(f"{API_BASE}/persons/{passport}", timeout=5)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


# ---------- Sidebar: filters ----------
st.sidebar.header("Search filters")
search = st.sidebar.text_input("Full name contains")
city = st.sidebar.text_input("City (exact match)")
company = st.sidebar.text_input("Company (exact match)")
limit = st.sidebar.slider("Page size", 10, 200, 50, step=10)
page = st.sidebar.number_input("Page", min_value=1, value=1, step=1)
offset = (page - 1) * limit

# ---------- Stats overview ----------
try:
    stats = fetch_stats()
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total persons", f"{stats['total_persons']:,}")
    col_b.metric("Top cities tracked", len(stats["top_cities"]))
    col_c.metric("Top companies tracked", len(stats["top_companies"]))

    with st.expander("Top 10 cities"):
        st.dataframe(pd.DataFrame(stats["top_cities"]), width="stretch", hide_index=True)
    with st.expander("Top 10 companies"):
        st.dataframe(pd.DataFrame(stats["top_companies"]), width="stretch", hide_index=True)
    with st.expander("Top 10 jobs"):
        st.dataframe(pd.DataFrame(stats.get("top_jobs", [])), width="stretch", hide_index=True)
    with st.expander("Sex distribution"):
        st.dataframe(
            pd.DataFrame(stats.get("sex_distribution", [])),
            width="stretch",
            hide_index=True,
        )
except requests.RequestException as exc:
    st.error(f"Could not fetch stats: {exc}")
    st.stop()

st.divider()


# ---------- Person detail ----------
def _field(label: str, value) -> None:
    st.markdown(f"**{label}**")
    st.markdown(value if value else "_Not available_")


st.subheader("Person detail")
detail_query = st.text_input(
    "Search by passport, name, last name, full name, or email",
    help="Case-insensitive substring match across passport, name, last name, full name and email.",
)

person = None
if detail_query:
    results = fetch_persons(
        city="",
        company="",
        search=detail_query.strip(),
        limit=25,
        offset=0,
    )
    if results["total"] == 0:
        st.warning("No person matches that search.")
    elif results["total"] == 1:
        person = results["items"][0]
    else:
        st.info(f"Found {results['total']:,} matches — pick one to see details.")
        options = {
            f"{p['fullname']}  |  {p['email'] or '—'}  |  {p['passport']}": p
            for p in results["items"]
        }
        pick = st.selectbox("Matches", list(options.keys()))
        person = options[pick]

if person:
    sex_icon = {"M": "♂", "F": "♀"}.get(person.get("sex") or "", "•")
    st.markdown(f"## {sex_icon} {person.get('fullname') or 'Unnamed'}")
    st.caption(f"Passport: `{person['passport']}`")

    tab_contact, tab_work, tab_finance, tab_location = st.tabs(
        ["Contact", "Work", "Finance", "Location"]
    )

    with tab_contact:
        col1, col2 = st.columns(2)
        with col1:
            _field("Email", person.get("email"))
            _field("Phone", person.get("telfnumber"))
        with col2:
            _field("First name", person.get("name"))
            _field("Last name", person.get("last_name"))

    with tab_work:
        col1, col2 = st.columns(2)
        with col1:
            _field("Company", person.get("company"))
            _field("Job title", person.get("job"))
            _field("Company email", person.get("company_email"))
        with col2:
            _field("Company phone", person.get("company_telfnumber"))
            _field("Company address", person.get("company_address"))

    with tab_finance:
        col1, col2 = st.columns(2)
        with col1:
            _field("IBAN", f"`{person['IBAN']}`" if person.get("IBAN") else None)
        with col2:
            _field("Salary", person.get("salary"))

    with tab_location:
        col1, col2 = st.columns(2)
        with col1:
            _field("City", person.get("city"))
            _field("Address", person.get("address"))
        with col2:
            _field("IP address", f"`{person['IPv4']}`" if person.get("IPv4") else None)

st.divider()

# ---------- Person list ----------
st.subheader("Persons")
try:
    data = fetch_persons(city, company, search, limit, offset)
except requests.RequestException as exc:
    st.error(f"Could not fetch persons: {exc}")
    st.stop()

st.caption(
    f"Showing {len(data['items'])} of {data['total']:,} matches "
    f"(page {page}, offset {offset})"
)

if data["items"]:
    df = pd.DataFrame(data["items"])
    display_cols = ["passport", "fullname", "city", "company", "job", "email", "IPv4"]
    df = df[[c for c in display_cols if c in df.columns]]
    st.dataframe(df, width="stretch", hide_index=True)
else:
    st.info("No matches for the current filters.")
