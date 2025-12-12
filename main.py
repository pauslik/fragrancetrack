import os
import polars as pl
from nicegui import app, ui
from src.database import Tracker
from src.algolia import search_designers, search_fragrance


current_dir = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(current_dir, "db/cards")
# Read from environment variable, fallback to a dev key if missing
storage_secret = os.environ.get('NICEGUI_SECRET', 'dev-secret-key-do-not-use-in-prod')


app.add_static_files('/cards', image_dir)
# ui.dark_mode(True)

# Create sample dataframe
db = Tracker("tracker_db.json")

# Home page
@ui.page('/')
def home():
    ui.label('FragranceTrack').classes('text-2xl')
    ui.link('My Fragrances', '/my_frags')
    ui.link('Search Online', '/search')

# ====================================================================
# search page of your own fragrances
@ui.page('/my_frags')
def my_frags_page():
    with ui.row().classes('w-full items-center mb-4'):
        ui.label('My Fragrances').classes('text-2xl mb-4')
        ui.space()
        ui.link('<- Home', '/')
    
    @ui.refreshable
    def build_grid(data: pl.DataFrame):
    # 3 items per row with gap-4 spacing
        with ui.grid().classes('grid-cols-3 gap-4 w-full'):
            for row in data.iter_rows(named=True):
                with ui.card().classes('w-fullcursor-pointer hover:bg-gray-100') \
                        .on('click', lambda e, perfume=row: open_add_frag(perfume)):           
                    # abspath to web URL
                    filename = os.path.basename(row['card'])
                    image_url = f'/cards/{filename}'
                    # display card
                    ui.image(image_url).classes('w-full object-contain')
                    # display text
                    with ui.card_section().classes('w-full'):
                        with ui.row().classes('w-full items-center no-wrap'):
                            with ui.column().classes('gap-0'):
                                ui.label(row['brand']).classes('text-lg font-bold')
                                ui.label(row['name']).classes('text-gray-500')
                            ui.space()
                            with ui.column().classes('items-center gap-0'):
                                ui.label('My Score:').classes('text-lg font-bold uppercase')
                                ui.label(str(row['my_score'])).classes('text-red-600 text-2xl font-bold leading-none')

    # >>>HANDLERS<<<
    # filtering logic which updates the display
    def update_filter(e):
        value = e.value
        # If search is empty, clear the grid
        if not value:
            filtered_df = db.df.head(0) 
        else:
            value = e.value
            if value:
                # TODO add a full_name column in the df and search that instead
                filtered_df = db.df.filter(
                    pl.col("brand").str.to_lowercase().str.contains(value.lower()) | 
                    pl.col("name").str.to_lowercase().str.contains(value.lower())
                )
        # limit to 3 rows
        filtered_df = filtered_df.head(9)
        # 3. Update the table's data
        build_grid.refresh(filtered_df)

    def open_add_frag(perfume):
        app.storage.user['selected_perfume'] = perfume
        app.storage.user['prev_page'] = '/my_frags'
        ui.navigate.to('/add_frag')


    # interactive search for brand/name
    ui.input('Search by Brand/Name', on_change=update_filter) \
        .classes('w-full max-w-xs mb-4') \
        .props('clearable')
    
    # start with empty df to not display all items when opened
    build_grid(db.df.head(0))

# ====================================================================
# Fragrantica.com online search (for new fragrances)
@ui.page('/search')
def search_page():
    with ui.row().classes('w-full items-center mb-4'):
        ui.label('Fragrantica Search').classes('text-2xl mb-4')
        ui.space()
        ui.link('<- Home', '/')
    # dict in case we would want to pass more variables returned from the search, like ID
    selected_brand = {'brand': None} 

    @ui.refreshable
    def brands(results_list):
        # Check if list is empty or None
        if not results_list:
            if results_list is not None:
                ui.label('No results found.').classes('text-gray-500 italic')
            return
        with ui.grid().classes('grid-cols-3 gap-4 w-full'):
            # not limiting results, algolia function should already return a limited result
            for item in results_list:
                with ui.card().classes('w-full cursor-pointer hover:bg-gray-100') \
                        .on('click', lambda e, designer=item: select_brand(designer)):
                    # TODO figure out how to get images
                    with ui.card_section():
                        ui.label(item['brand']).classes('text-lg font-bold')

    @ui.refreshable
    def perfumes(results_list):
        # Don't show anything until a brand is picked
        if not selected_brand['brand']:
            return
        ui.separator().classes('my-8')
        # ui.label(f"Perfumes from: {selected_brand['brand']}").classes('text-xl font-bold text-blue-600')

        if not results_list:
            if results_list is not None:
                ui.label('No results found.').classes('text-gray-500 italic')
            return
        with ui.grid().classes('grid-cols-5 gap-4 w-full'):
            # not limiting results, algolia function should already return a limited result
            for item in results_list:
                with ui.card().classes('w-full cursor-pointer hover:bg-gray-100') \
                        .on('click', lambda e, perfume=item: open_add_frag(perfume)):
                    # display picture ('thumb' is way too small)
                    ui.image(item['picture']).classes('w-full object-scale-down')
                    with ui.card_section():
                        ui.label(item['name']).classes('text-lg font-bold')

    @ui.refreshable
    def perfume_search_area():
        # If no brand is selected, hide this whole section
        if not selected_brand['brand']:
            return
        ui.separator().classes('my-8')
        # ui.label(f"Perfumes from: {selected_brand['brand']}").classes('text-xl font-bold text-blue-600')

        # handle input from perfume name search
        def handle_perfume_search():
            p_name = p_input.value
            results = search_fragrance(selected_brand['brand'], p_name)
            perfumes.refresh(results)

        # refresh after input
        p_input = ui.input('Perfume Name').on('keypress.enter', handle_perfume_search).classes('w-full max-w-xs mb-4')
        perfumes(None)
    
    # >>>HANDLERS<<<
    # show secondary search after selection
    def select_brand(designer):
        selected_brand['brand'] = designer['brand']
        # hide the brand results after selection
        brands.refresh(None)
        perfume_search_area.refresh()

    # search for brands with input and update with results
    def handle_brand_search():
        query = b_input.value.strip()
        # clear results if empty search
        if not query:
            brands.refresh(None)
            return
        
        results = search_designers(query) 
        brands.refresh(results)
    
    # Save the entire dictionary to user session
    def open_add_frag(perfume):
        app.storage.user['selected_perfume'] = perfume
        app.storage.user['prev_page'] = '/search'
        ui.navigate.to('/add_frag')

    # brand search input
    b_input = ui.input('Search Brand').on('keypress.enter', handle_brand_search)
    # start with empty list
    brands(None)
    # perfume search are initially hidden
    perfume_search_area()

# ====================================================================
# add found fragrance to your collection
@ui.page('/add_frag')
def add_frag_page():
    # Retrieve data
    perfume = app.storage.user.get('selected_perfume')
    prev_page = app.storage.user.get('prev_page')
    if not prev_page:
        prev_page = '/'
    if not perfume:
        ui.label('No perfume selected.').classes('text-red-500')
        ui.link('Go back', prev_page)
        return
    # if we already have this fragrance, get it's details from our DB, otherwise - from fragrantica
    matches = db.df.filter((db.df['brand'] == perfume['brand']) & (db.df['name'] == perfume['name']))
    if not matches.is_empty():
        my_score = matches.select("my_score").item(0, 0)
        filename = os.path.basename(matches.select("card").item(0, 0))
        card = f'/cards/{filename}'
    else:
        card = f'https://www.fragrantica.com/mdimg/perfume-social-cards/en-p_c_{perfume['id']}.jpeg'
        my_score = None
    
    with ui.row().classes('w-full'):
        ui.label('Add/Update fragrance').classes('text-xl') 
        ui.link('<- Back', prev_page).classes('ml-auto') 
    
    with ui.row().classes('w-full gap-8'):
        # Left: Image
        ui.image(card).classes('w-64 rounded-lg shadow-lg')
        
        # Right: Details
        with ui.column():
            ui.label(perfume['name']).classes('text-4xl font-bold')
            ui.label(perfume['brand']).classes('text-xl text-gray-500')
            ui.separator().classes('my-4')
            # displaying score input
            with ui.column().classes('gap-2'):
                ui.label('My Score:').classes('font-bold')
                score_input = ui.number(value=my_score, min=0, max=10, precision=1).classes('text-2xl text-red-600 font-bold')
            
            # >>>HANDLERS<<<
            # check input and add/update fragrance
            def handle_save():
                if score_input.value is None:
                    ui.notify('Please enter a score', type='warning')
                    return
                db.update_fragrance(perfume['brand'], perfume['name'], int(score_input.value))
                ui.notify(f"Saved", type='positive')

            ui.button('Save', on_click=handle_save)


# ====================================================================
# Run with FastAPI integration
ui.run_with(
    app,
    storage_secret=storage_secret)

if __name__ in {"__main__", "__mp_main__"}:
    ui.run()
