# VoronoiGen
### Team Mahjong | CSCI 4440 - Software Design & Documentation

VoronoiGen is a desktop application for generating and customizing Voronoi diagrams. Users can create diagrams from scratch or load site data from CSV/Excel files, assign labels and colors to cells, and export the result as an image.

---

## Features 

- **Voronoi Diagram Generation** — Add, remove, and reposition sites on a canvas to generate Voronoi cells in real time
- **Label Manager** — Create and manage labels with custom fill and site colors to categorize cells
- **Cell Customization** — Select individual cells to change their fill color, site color, label, and position
- **Canvas Options** — Toggle cell border lines and site points, change line color, and adjust line thickness
- **File Support** — Load site data from CSV or Excel files, or open/save projects in the custom `.noi` format
- **Export** — Export the diagram as a PNG, JPEG, or BMP image

---

## Requirements

- Python 3.10+
- PySide6
- Shapely
- Pandas
  
---

## Usage

### Creating a New Project
1. Click **Create New Project** on the home screen
2. Enter a project name, canvas width, and canvas height
3. Optionally load a CSV or Excel file with site data
4. Click **OK** to open the main canvas

### Opening an Existing Project
1. Click **Open Project** on the home screen
2. Select a `.noi` file to load a previously saved project

### Adding and Removing Sites
- Select **Add Site** mode and click anywhere on the canvas to place a new site
- Select **Remove Site** mode and click on a cell to remove its site

### Customizing Cells
- Select **Select Cell** mode and click on a cell to open the customization dialog
- Change the cell's fill color, site color, label, or position

### Canvas Options
- **Lines ON/OFF** — Toggle the visibility of cell border lines
- **Pick Color** — Change the color of cell border lines
- **Line Thickness** — Adjust border line thickness using the slider or spinbox
- **Sites ON/OFF** — Toggle the visibility of site points

### Labels
- Click **+ Add Label** to create a new label
- Click a label to select it — new sites will be assigned to the selected label
- Use **Edit**, **Color**, and **Del** buttons to manage existing labels

### Saving and Exporting
- **File → Save Project** — Save the current project as a `.noi` file
- **File → Export Diagram** — Export the canvas as a PNG, JPEG, or BMP image

---

## File Format

### CSV / Excel
Each row represents a site with the following columns:

| Column | Description |
|--------|-------------|
| 1 | X coordinate |
| 2 | Y coordinate |
| 3 | Label name (optional) |
| 4 | Cell fill color as hex (optional) |
| 5 | Site color as hex (optional) |

### .noi (VoronoiGen project file)
A custom CSV-based format that stores canvas dimensions, project title, and all site data.

---
