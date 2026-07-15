from langchain_core.documents import Document

from server.tools.llm import llm


GROUP_SIZE = 15


def _split_list(items: list, group_size: int) -> list[list]:

    """
    Split a list into smaller groups.
    """

    return [

        items[index : index + group_size]

        for index in range(0, len(items), group_size)

    ]


def _summarize_documents(
    documents: list[Document]
) -> str:

    """
    Summarize a group of document chunks.
    """

    context = "\n\n".join(

        document.page_content

        for document in documents

    )

    prompt = f"""

You are an expert AI tutor.

Convert the following pages into structured study notes.

Rules:

• Keep every important concept.

• Remove repetitive explanations.

• Remove unnecessary stories.

• Preserve definitions.

• Preserve formulas.

• Preserve algorithms.

• Preserve important examples only.

• Use headings.

• Use bullet points.

• Maximum 400 words.

Document:

{context}

"""

    response = llm.invoke(prompt)

    return response.content


def _merge_group(
    summaries: list[str]
) -> str:

    """
    Merge a small group of summaries.
    """

    context = "\n\n".join(summaries)

    prompt = f"""
You are merging multiple study notes.

Instructions:

• Merge related headings.

• Remove repetition.

• Compress the content by about 30%.

• Preserve every important concept.

• Use headings.

• Use bullets.

• Maximum 500 words.

Study Notes:

{context}
"""

    response = llm.invoke(prompt)

    return response.content


def summarize_document(
    chunks: list[Document]
) -> str:

    """
    Hierarchical summarization.

    Keeps merging summaries until only one summary remains.
    """

    print("Starting hierarchical summarization...")

    # ---------- Level 1 ----------

    groups = _split_list(

        chunks,

        GROUP_SIZE

    )

    summaries = []

    for index, group in enumerate(groups):

        print(

            f"Summarizing group {index + 1}/{len(groups)}"

        )

        summaries.append(

            _summarize_documents(group)

        )

    level = 2

    # ---------- Higher Levels ----------

    while len(summaries) > 1:

        print(

            f"Merging Level {level} ({len(summaries)} summaries)"

        )

        summary_groups = _split_list(

            summaries,

            GROUP_SIZE

        )

        merged_summaries = []

        for index, group in enumerate(summary_groups):

            print(

                f"  Merge {index + 1}/{len(summary_groups)}"

            )

            merged_summaries.append(

                _merge_group(group)

            )

        summaries = merged_summaries

        level += 1

    print("Summary completed.")

    return summaries[0]


