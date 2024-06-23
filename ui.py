import streamlit as st
from utils.save_load import save_json, load_json, list_files_in_dir, list_chapters_in_file, add_chapter, delete_chapter
from os.path import join, exists
import os

st.set_page_config(
    page_title="Main"
)

stories_path = './stories/'
if not exists(stories_path):
    os.mkdir(stories_path)
if not exists(join(stories_path, 'deleted')):
    os.mkdir(join(stories_path, 'deleted'))
if not list_files_in_dir(stories_path):
    save_json(join(stories_path, 'example.json'), {'title': 'example', 'content': '', 'chapters': []})

# remove padding around the main container
st.markdown("""
        <style>
               #root > div:nth-child(1) > div > div > div > div > section > div {
                    max-width: none;
                }
        </style>
        """, unsafe_allow_html=True)

if 'list_in_dir' not in st.session_state:
    st.session_state.list_in_dir = list_files_in_dir(stories_path)

with st.sidebar:
    st.selectbox(
        'What file would you like to edit?',
        st.session_state.list_in_dir,
        key='file'
    )
    file_path = join(stories_path, st.session_state.file)
    data = load_json(file_path)
    
    col1, col2 = st.columns(2)
    
    with st.popover("File Settings"):
        st.markdown("Create new file")
        file_name = st.text_input("What's the name of the file?")
        if st.button("Create"):
            save_json(join(stories_path, file_name + '.json'), {'title': file_name, 'content': '', 'chapters': []})
            st.session_state.list_in_dir = list_files_in_dir(stories_path)
            st.rerun()
        if st.button("Delete File"):
            os.rename(file_path, join(stories_path, 'deleted', st.session_state.file))
            st.session_state.list_in_dir = list_files_in_dir(stories_path)
            st.rerun()

tab1, tab2  = st.tabs(["Editor", "Chapter"])
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        def textbox_onchange():
            data['title'] = st.session_state.title
            data['content'] = st.session_state.content
            save_json(file_path, data)
        st.text_input('Title', key='title', on_change=textbox_onchange, value=load_json(file_path)['title'])
        st.text_area('Content', key='content', on_change=textbox_onchange, value=load_json(file_path)['content'])
    with col2:
        st.write("Content of file:", st.session_state.file)
        st.write(data)

# ensure st.session_state.chapter is initialized
if 'chapter' not in st.session_state:
    st.session_state.chapter = data['chapters'][0]['title'] if data['chapters'] else ''

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        def chapterbox_onchange():
            for i in range(len(data['chapters'])):
                if data['chapters'][i]['title'] == st.session_state.chapter:
                    data['chapters'][i]['content'] = st.session_state.chapter_content
                    save_json(file_path, data)
                    break
        for chapter in data['chapters']:
            if chapter['title'] == st.session_state.chapter:
                st.text_area('Content', key='chapter_content', on_change=chapterbox_onchange, value=chapter['content'])
                break
    with col2:
        st.selectbox('Chapters', [chapter['title'] for chapter in data['chapters']], key='chapter')
        with st.popover("Chapter Settings"):
            st.markdown("Create new chapter")
            chapter_name = st.text_input("What's the name of the chapter?")
            if st.button('Add chapter'): add_chapter(file_path, chapter_name)
            if st.button('Delete Chapter'): delete_chapter(file_path, st.session_state.chapter)
        st.write("Chapters in file:", list_chapters_in_file(file_path))
        
        tab1, tab2, tab3  = st.tabs(["Codex", "Snippets", "Chats"])
        with tab1:
            with st.popover("+"):
                sb_type = st.selectbox('Type', ['Person', 'Location', 'Item', 'Lore', 'Subplot', 'Other'])
                sb_name = st.text_input("Name")
                sb_desc = st.text_area("Description")
                if st.button("Add"):
                    if 'data' not in data:
                        data['data'] = {'codex': [], 'snippets': [], 'chats': []}
                    data['data']['codex'].append({'type': sb_type, 'name': sb_name, 'description': sb_desc})
                    save_json(file_path, data)
                    st.rerun()
        with tab2:
            pass
        with tab3:
            pass