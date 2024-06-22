import streamlit as st
from utils.save_load import save_json, load_json, list_files_in_dir, list_chapters_in_file
from os.path import join, abspath
import os

st.set_page_config(
    page_title="Main"
)

stories_path = './stories/'
if not os.path.exists(stories_path):
    os.mkdir(stories_path)

# remove padding around the main container
st.markdown("""
        <style>
               #root > div:nth-child(1) > div > div > div > div > section > div {
                    max-width: none;
                }
        </style>
        """, unsafe_allow_html=True)

with st.sidebar:
    selectbox = st.selectbox(
        'What file would you like to edit?',
        list_files_in_dir(stories_path),
        key='file'
    )
    file_path = join(stories_path, st.session_state.file)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.popover("Create File"):
            st.markdown("Create new file")
            file_name = st.text_input("What's the name of the file?")
            if st.button("Create"):
                save_json(join(stories_path, file_name + '.json'), {'title': file_name, 'content': '', 'chapters': []})
                st.rerun()
    with col2:
        if st.button("Delete File"):
            # move file to stories/deleted
            if not os.path.exists(join(stories_path, 'deleted')):
                os.mkdir(join(stories_path, 'deleted'))
            os.rename(file_path, join(stories_path, 'deleted', st.session_state.file))
            st.rerun()

tab1, tab2  = st.tabs(["Editor", "Chapter"])
data = load_json(file_path)


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
        st.write(load_json(join(stories_path, st.session_state.file)))

# Ensure st.session_state.chapter is initialized
if 'chapter' not in st.session_state:
    st.session_state.chapter = data['chapters'][0]['title'] if data['chapters'] else ''

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        def chapterbox_onchange():
            for i in range(len(data['chapters'])):
                if data['chapters'][i]['title'] == st.session_state.chapter:
                    data['chapters'][i]['content'] = st.session_state.chapter_content
                    save_json(join(stories_path, st.session_state.file), data)
                    break
        for chapter in data['chapters']:
            if chapter['title'] == st.session_state.chapter:
                st.text_area('Content', key='chapter_content', on_change=chapterbox_onchange, value=chapter['content'])
                break
    with col2:
        right_col1, right_col2 = st.columns(2)
        with right_col1:
            with st.popover("Create Chapter"):
                st.markdown("Create new chapter")
                chapter_name = st.text_input("What's the name of the chapter?")
                if st.button('Add chapter'):
                    data['chapters'].append({'title': chapter_name, 'content': ''})
                    save_json(join(stories_path, st.session_state.file), data)
        with right_col2:
            if st.button('Delete Chapter'):
                for i in range(len(data['chapters'])):
                    if data['chapters'][i]['title'] == st.session_state.chapter:
                        data['chapters'].pop(i)
                        break
                save_json(join(stories_path, st.session_state.file), data)
        st.selectbox('Chapters', [chapter['title'] for chapter in data['chapters']], key='chapter')
        st.write("Chapters in file:", list_chapters_in_file(file_path))
