import streamlit as st
from utils.save_load import save_json, load_json, list_files_in_dir, list_chapters_in_file
from os.path import join, exists
import os

st.set_page_config(
    page_title="Main"
)

example_json = {'title': 'example', 'content': '', 'chapters': [], 'data': {'codex': [], 'snippets': [], 'chats': []}}
stories_path = './stories/'
if not exists(stories_path):
    os.mkdir(stories_path)
if not exists(join(stories_path, 'deleted')):
    os.mkdir(join(stories_path, 'deleted'))
if not list_files_in_dir(stories_path):
    save_json(join(stories_path, 'example.json'), example_json)

# remove padding around the main container
st.markdown("""
        <style>
               #root > div:nth-child(1) > div > div > div > div > section > div {
                    max-width: none;
                }
        </style>
        """, unsafe_allow_html=True)

def setState(key, value):
    st.session_state[key] = value

if 'list_in_dir' not in st.session_state:
    setState('list_in_dir', list_files_in_dir(stories_path))

with st.sidebar:
    def selectbox_onchange():
        setState('json_data', load_json(join(stories_path, st.session_state.file)))
    st.selectbox(
        'What file would you like to edit?',
        st.session_state.list_in_dir,
        key='file',
        on_change=selectbox_onchange
    )
    file_path = join(stories_path, st.session_state.file)
    if 'json_data' not in st.session_state:
        setState('json_data', load_json(file_path))
    data = st.session_state.json_data
    
    col1, col2 = st.columns(2)
    with st.popover("File Settings"):
        st.markdown("Create new file")
        file_name = st.text_input("What's the name of the file?")
        def button_onclick():
            setState('list_in_dir', list_files_in_dir(stories_path))
        if st.button("Create", on_click=button_onclick):
            example_json['title'] = file_name
            save_json(join(stories_path, file_name + '.json'), example_json)
        if st.button("Delete File", on_click=button_onclick):
            os.rename(file_path, join(stories_path, 'deleted', st.session_state.file))

tab1, tab2  = st.tabs(["Editor", "Chapter"])
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        def textbox_onchange():
            setState('title', st.session_state.title)
            setState('content', st.session_state.content)
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
            if st.button('Add chapter'):
                data['chapters'].append({'title': chapter_name, 'content': ''})
                save_json(file_path, data)
            if st.button('Delete chapter'):
                for i in range(len(data)):
                    if data['chapters'][i]['title'] == st.session_state.chapter:
                        save_json(join('stories', 'deleted', 'deleted-chapters.json'), data['chapters'][i], mode='a')
                        data['chapters'].pop(i)
                        break
                save_json(file_path, data)
        st.write("Chapters in file:", list_chapters_in_file(file_path))
        
        tab1, tab2, tab3  = st.tabs(["Codex", "Snippets", "Chats"])
        with tab1:
            with st.popover("Add"):
                sb_type = st.selectbox('Type', ['Person', 'Location', 'Item', 'Lore', 'Subplot', 'Other'])
                sb_name = st.text_input("Name")
                sb_desc = st.text_area("Description")
                if st.button("Add"):
                    data['data']['codex'].append({'type': sb_type, 'name': sb_name, 'description': sb_desc})
                    save_json(file_path, data)
                    st.rerun()
        with tab2:
            pass
        with tab3:
            pass