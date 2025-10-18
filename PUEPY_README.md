# What Would Jesse Do? - PuePy Application

This memorial website has been refactored as a PuePy application, following the same pattern as the Garden Blog.

## Structure

### Content (Markdown Files)

All content is stored as markdown files in the `doc/` directory:

- **`doc/jesse-*.md`** - Main life section narratives (childhood, teen years, etc.)
- **`doc/jesse-eulogy-intro.md`** - Introduction to the eulogy
- **`doc/jesse-eulogy-final-thoughts.md`** - Final thoughts
- **`doc/topics/`** - Individual memory cards/topics, organized by category

Each markdown file includes metadata:
```markdown
Title: Card Title
Date: 02025-04-04
Author: Author Name <optional-orcid>
Years: 01981,01982,01983
```

### Application Files

- **`index.html`** - Entry point, loads PyScript and main.py
- **`pyscript.json`** - Configuration listing all markdown files to load
- **`src/main.py`** - Main application with routing
- **`src/common.py`** - Reusable components and data loading
- **`src/topics.py`** - Legacy file (kept for compatibility with generate.py)

### Routes

The application uses hash-based routing:

- **`#/`** - Home page with full eulogy
- **`#/years/<year>`** - Year-specific page (e.g., `#/years/1985`)
- **`#/life/<section_id>`** - Individual life section page
- **`#/about`** - About page (coming soon)

### Components

Defined in `src/common.py`:

- **NavBar** - Navigation with dropdowns for life sections and timeline
- **TopicCard** - Displays a memory/topic card from markdown
- **WWJDWidget** - "What Would Jesse Do" list with reveal functionality
- **LifeSection** - Renders a life section from markdown
- **Footer** - Simple footer

### Data Loading

The application automatically loads:

1. **All topics** from `doc/topics/` subdirectories
2. **Life sections** defined in `LIFE_SECTIONS` constant
3. **Markdown content** is parsed on-demand with metadata extraction
4. **Media** downloaded on demand from `static/` subdirectories 

## Development

### Local Testing

```bash
# Start a simple HTTP server
python3 -m http.server 8000

# Open browser to http://localhost:8000
```

### Adding New Content

1. **Add a new memory card:**
   - Create `doc/topics/<category>/<filename>.md`
   - Add metadata (Title, Author, Years)
   - Add file path to `pyscript.json`

2. **Edit life sections:**
   - Directly edit the markdown files in `doc/`
   - No need to regenerate - changes load dynamically

### Static Site Generation

The old static site generator (`src/generate.py`) is preserved but the site now runs as a dynamic PuePy application. To generate static files (for backwards compatibility):

```bash
python src/generate.py /what-would-jesse-do
```

## Dependencies

Loaded via PyScript:
- **puepy** - Python frontend framework
- **markdown** - Markdown to HTML conversion
- **morphdom** - DOM diffing (for PuePy)

Frontend:
- **Bootstrap 5.3.3** - CSS framework
- **PyScript 2025.8.1** - Python in the browser

## Comparison to Garden Blog

This project follows the same pattern as the Garden Blog:

| Feature | Garden Blog | WWJD |
|---------|-------------|------|
| Content organization | `posts/YYYY/MM-DD.md` | `doc/topics/<category>/<name>.md` |
| Component pattern | `@t.component()` decorators | Same |
| Routing | Hash-based with year/post | Hash-based with year/section |
| Data loading | Auto-scan post directories | Manual topic list + auto-scan |
| Metadata | Via markdown.Meta | Same |

## License

Apache 2.0 - See LICENSE file
