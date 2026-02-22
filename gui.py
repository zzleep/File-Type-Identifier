"""
GUI Application for File Type Identification System
Provides a user-friendly graphical interface for detecting file types and mismatches.
Modern UI/UX Design with enhanced visuals and user experience.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
from typing import Optional

from src.filemagic import FileTypeDetector, FileTypeDatabase


class FileTypeIdentifierGUI:
    """Main GUI application for file type identification with modern UI/UX."""
    
    # Modern color palette
    COLORS = {
        'primary': '#2563eb',      # Modern blue
        'primary_hover': '#1d4ed8',
        'success': '#10b981',       # Green
        'warning': '#f59e0b',       # Amber
        'danger': '#ef4444',        # Red
        'bg_main': '#f8fafc',       # Light gray-blue
        'bg_card': '#ffffff',       # White
        'bg_secondary': '#f1f5f9',  # Lighter gray
        'text_primary': '#1e293b',  # Dark slate
        'text_secondary': '#64748b', # Medium slate
        'border': '#e2e8f0',        # Light border
        'accent': '#8b5cf6',        # Purple accent
    }
    
    def __init__(self, root):
        self.root = root
        self.root.title("File Type Identifier")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        
        # Set window background
        self.root.configure(bg=self.COLORS['bg_main'])
        
        # Initialize detector
        self.detector = FileTypeDetector()
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        
        # Center window
        self.center_window()
    
    def setup_styles(self):
        """Configure modern custom styles for widgets."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main background
        style.configure('.', background=self.COLORS['bg_main'])
        
        # Title styling - larger and more prominent
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 24, 'bold'), 
                       foreground=self.COLORS['primary'],
                       background=self.COLORS['bg_main'])
        
        # Subtitle styling
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 11),
                       foreground=self.COLORS['text_secondary'],
                       background=self.COLORS['bg_main'])
        
        # Section headers
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 11, 'bold'),
                       foreground=self.COLORS['text_primary'],
                       background=self.COLORS['bg_card'])
        
        # Card frame style
        style.configure('Card.TFrame',
                       background=self.COLORS['bg_card'],
                       relief='flat')
        
        # Main frame
        style.configure('Main.TFrame',
                       background=self.COLORS['bg_main'])
        
        # Primary button - modern look
        style.configure('Primary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground='white',
                       background=self.COLORS['primary'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(20, 10))
        style.map('Primary.TButton',
                 background=[('active', self.COLORS['primary_hover']),
                           ('pressed', self.COLORS['primary_hover'])])
        
        # Secondary button
        style.configure('Secondary.TButton',
                       font=('Segoe UI', 9),
                       background=self.COLORS['bg_secondary'],
                       foreground=self.COLORS['text_primary'],
                       borderwidth=1,
                       relief='solid',
                       padding=(15, 8))
        style.map('Secondary.TButton',
                 background=[('active', self.COLORS['border'])])
        
        # Entry styling
        style.configure('Modern.TEntry',
                       fieldbackground='white',
                       borderwidth=1,
                       relief='solid',
                       padding=8)
        
        # Notebook (tabs) styling
        style.configure('TNotebook',
                       background=self.COLORS['bg_main'],
                       borderwidth=0,
                       tabmargins=[10, 5, 10, 0])
        style.configure('TNotebook.Tab',
                       font=('Segoe UI', 10),
                       padding=[20, 10],
                       background=self.COLORS['bg_secondary'],
                       foreground=self.COLORS['text_secondary'])
        style.map('TNotebook.Tab',
                 background=[('selected', self.COLORS['bg_card'])],
                 foreground=[('selected', self.COLORS['primary'])],
                 expand=[('selected', [1, 1, 1, 0])])
        
        # Checkbutton styling
        style.configure('Modern.TCheckbutton',
                       font=('Segoe UI', 10),
                       background=self.COLORS['bg_card'],
                       foreground=self.COLORS['text_primary'])
        
        # Status bar
        style.configure('Status.TLabel',
                       font=('Segoe UI', 9),
                       background=self.COLORS['bg_secondary'],
                       foreground=self.COLORS['text_secondary'],
                       padding=(10, 5))
    
    def create_widgets(self):
        """Create all GUI widgets with modern design."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20", style='Main.TFrame')
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header section with icon and title
        header_frame = ttk.Frame(main_frame, style='Main.TFrame')
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Title with emoji icon
        title_label = ttk.Label(
            header_frame, 
            text="🔍 File Type Identifier", 
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(
            header_frame,
            text="Detect file types using magic numbers • Identify disguised files • Verify authenticity",
            style='Subtitle.TLabel'
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        
        # Stats badge (shows database info)
        stats_frame = ttk.Frame(header_frame, style='Main.TFrame')
        stats_frame.grid(row=0, column=1, rowspan=2, sticky=tk.E, padx=(20, 0))
        
        extensions_count = len(self.detector.database.get_supported_extensions())
        stats_label = ttk.Label(
            stats_frame,
            text=f"📊 {extensions_count}+ Supported Types",
            font=('Segoe UI', 10, 'bold'),
            foreground=self.COLORS['accent'],
            background=self.COLORS['bg_main']
        )
        stats_label.pack()
        
        header_frame.columnconfigure(1, weight=1)
        
        # Separator line
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Create notebook (tabbed interface) with card style
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        
        # Create tabs
        self.create_file_analysis_tab()
        self.create_directory_analysis_tab()
        self.create_database_info_tab()
        
        # Modern status bar with icon
        status_frame = ttk.Frame(main_frame, style='Main.TFrame')
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        status_card = ttk.Frame(status_frame, relief='flat', style='Card.TFrame', padding="10")
        status_card.pack(fill=tk.X)
        
        self.status_var = tk.StringVar(value="✓ Ready to analyze files")
        self.status_label = ttk.Label(
            status_card, 
            textvariable=self.status_var, 
            style='Status.TLabel'
        )
        self.status_label.pack(side=tk.LEFT)
    
    def create_file_analysis_tab(self):
        """Create the single file analysis tab with modern design."""
        tab = ttk.Frame(self.notebook, padding="20", style='Card.TFrame')
        self.notebook.add(tab, text="📄 Single File")
        
        # Configure grid
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(4, weight=1)
        
        # Info card at top
        info_frame = ttk.Frame(tab, style='Card.TFrame', relief='solid', borderwidth=1, padding="15")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(
            info_frame,
            text="💡 Tip: Select any file to analyze its true file type using magic number detection",
            font=('Segoe UI', 9),
            foreground=self.COLORS['text_secondary'],
            background=self.COLORS['bg_card']
        ).pack(anchor=tk.W)
        
        # File selection section
        ttk.Label(tab, text="Select File", style='Header.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=(0, 8)
        )
        
        file_frame = ttk.Frame(tab, style='Card.TFrame')
        file_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        file_frame.columnconfigure(0, weight=1)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(
            file_frame, 
            textvariable=self.file_path_var,
            font=('Segoe UI', 10),
            style='Modern.TEntry'
        )
        file_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_btn = ttk.Button(
            file_frame, 
            text="📁 Browse", 
            command=self.browse_file,
            style='Secondary.TButton'
        )
        browse_btn.grid(row=0, column=1)
        
        # Analyze button - prominent
        analyze_btn = ttk.Button(
            tab, 
            text="🔍 Analyze File", 
            command=self.analyze_file,
            style='Primary.TButton'
        )
        analyze_btn.grid(row=3, column=0, pady=(0, 20))
        
        # Results section
        results_header = ttk.Frame(tab, style='Card.TFrame')
        results_header.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        
        ttk.Label(results_header, text="Analysis Results", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Results area with modern styling
        results_container = ttk.Frame(tab, relief='solid', borderwidth=1, style='Card.TFrame')
        results_container.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.file_results_text = scrolledtext.ScrolledText(
            results_container,
            wrap=tk.WORD,
            width=80,
            height=18,
            font=('Consolas', 10),
            bg='white',
            fg=self.COLORS['text_primary'],
            relief='flat',
            padx=10,
            pady=10,
            borderwidth=0
        )
        self.file_results_text.pack(fill=tk.BOTH, expand=True)
        
        # Add placeholder text
        placeholder = "Select a file and click 'Analyze File' to see detailed results here.\n\n"
        placeholder += "The analysis will show:\n"
        placeholder += "  • File path and name\n"
        placeholder += "  • Claimed file extension\n"
        placeholder += "  • Detected file type (via magic numbers)\n"
        placeholder += "  • MIME type\n"
        placeholder += "  • Confidence level\n"
        placeholder += "  • Mismatch warnings (if any)\n"
        self.file_results_text.insert(1.0, placeholder)
        self.file_results_text.config(state=tk.DISABLED)
        
        tab.rowconfigure(5, weight=1)
    
    def create_directory_analysis_tab(self):
        """Create the directory analysis tab with modern design."""
        tab = ttk.Frame(self.notebook, padding="20", style='Card.TFrame')
        self.notebook.add(tab, text="📁 Directory Scan")
        
        # Configure grid
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(5, weight=1)
        
        # Info card
        info_frame = ttk.Frame(tab, style='Card.TFrame', relief='solid', borderwidth=1, padding="15")
        info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(
            info_frame,
            text="💡 Tip: Scan entire folders to find disguised or misnamed files in bulk",
            font=('Segoe UI', 9),
            foreground=self.COLORS['text_secondary'],
            background=self.COLORS['bg_card']
        ).pack(anchor=tk.W)
        
        # Directory selection
        ttk.Label(tab, text="Select Directory", style='Header.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=(0, 8)
        )
        
        dir_frame = ttk.Frame(tab, style='Card.TFrame')
        dir_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        dir_frame.columnconfigure(0, weight=1)
        
        self.dir_path_var = tk.StringVar()
        dir_entry = ttk.Entry(
            dir_frame, 
            textvariable=self.dir_path_var,
            font=('Segoe UI', 10),
            style='Modern.TEntry'
        )
        dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        browse_dir_btn = ttk.Button(
            dir_frame, 
            text="📁 Browse", 
            command=self.browse_directory,
            style='Secondary.TButton'
        )
        browse_dir_btn.grid(row=0, column=1)
        
        # Options section
        options_frame = ttk.Frame(tab, style='Card.TFrame', relief='solid', borderwidth=1, padding="12")
        options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Label(
            options_frame,
            text="Scan Options",
            font=('Segoe UI', 9, 'bold'),
            foreground=self.COLORS['text_primary'],
            background=self.COLORS['bg_card']
        ).pack(anchor=tk.W, pady=(0, 8))
        
        self.recursive_var = tk.BooleanVar(value=False)
        recursive_check = ttk.Checkbutton(
            options_frame,
            text="🔄 Include subdirectories (recursive scan)",
            variable=self.recursive_var,
            style='Modern.TCheckbutton'
        )
        recursive_check.pack(anchor=tk.W)
        
        # Analyze button
        analyze_dir_btn = ttk.Button(
            tab, 
            text="🔍 Analyze Directory", 
            command=self.analyze_directory,
            style='Primary.TButton'
        )
        analyze_dir_btn.grid(row=4, column=0, pady=(0, 20))
        
        # Results section
        results_header = ttk.Frame(tab, style='Card.TFrame')
        results_header.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 8))
        
        ttk.Label(results_header, text="Scan Results", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Results area
        results_container = ttk.Frame(tab, relief='solid', borderwidth=1, style='Card.TFrame')
        results_container.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.dir_results_text = scrolledtext.ScrolledText(
            results_container,
            wrap=tk.WORD,
            width=80,
            height=18,
            font=('Consolas', 10),
            bg='white',
            fg=self.COLORS['text_primary'],
            relief='flat',
            padx=10,
            pady=10,
            borderwidth=0
        )
        self.dir_results_text.pack(fill=tk.BOTH, expand=True)
        
        # Add placeholder
        placeholder = "Select a directory and click 'Analyze Directory' to scan all files.\n\n"
        placeholder += "The scan will show:\n"
        placeholder += "  • Total files analyzed\n"
        placeholder += "  • Number of mismatches found\n"
        placeholder += "  • Detection confidence statistics\n"
        placeholder += "  • Detailed results for each file\n\n"
        placeholder += "Enable recursive scan to include all subdirectories.\n"
        self.dir_results_text.insert(1.0, placeholder)
        self.dir_results_text.config(state=tk.DISABLED)
        
        tab.rowconfigure(6, weight=1)
    
    def create_database_info_tab(self):
        """Create the database information tab with modern design."""
        tab = ttk.Frame(self.notebook, padding="20", style='Card.TFrame')
        self.notebook.add(tab, text="📊 Database Info")
        
        # Configure grid
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)
        
        # Header section
        ttk.Label(
            tab, 
            text="Supported File Types Database", 
            style='Header.TLabel'
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        # Statistics cards
        stats_container = ttk.Frame(tab, style='Card.TFrame')
        stats_container.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        extensions = self.detector.database.get_supported_extensions()
        signatures_count = len(self.detector.database)
        extensions_count = len(extensions)
        
        # Create stat cards
        stats_data = [
            ("🔢 Total Signatures", str(signatures_count), self.COLORS['primary']),
            ("📄 File Extensions", f"{extensions_count}+", self.COLORS['success']),
            ("🎯 Detection Method", "Magic Numbers", self.COLORS['accent'])
        ]
        
        for i, (label, value, color) in enumerate(stats_data):
            card = ttk.Frame(stats_container, relief='solid', borderwidth=1, padding="15", style='Card.TFrame')
            card.grid(row=0, column=i, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10 if i < 2 else 0))
            
            ttk.Label(
                card,
                text=label,
                font=('Segoe UI', 9),
                foreground=self.COLORS['text_secondary'],
                background=self.COLORS['bg_card']
            ).pack(anchor=tk.W)
            
            ttk.Label(
                card,
                text=value,
                font=('Segoe UI', 18, 'bold'),
                foreground=color,
                background=self.COLORS['bg_card']
            ).pack(anchor=tk.W, pady=(5, 0))
            
            stats_container.columnconfigure(i, weight=1)
        
        # Extensions header
        ttk.Label(
            tab,
            text="All Supported Extensions",
            style='Header.TLabel'
        ).grid(row=2, column=0, sticky=tk.W, pady=(0, 8))
        
        # Extensions list with modern styling
        extensions_container = ttk.Frame(tab, relief='solid', borderwidth=1, style='Card.TFrame')
        extensions_container.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.db_text = scrolledtext.ScrolledText(
            extensions_container,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=('Consolas', 10),
            bg='white',
            fg=self.COLORS['text_primary'],
            relief='flat',
            padx=10,
            pady=10,
            borderwidth=0
        )
        self.db_text.pack(fill=tk.BOTH, expand=True)
        
        # Populate database info
        self.populate_database_info()
        
        tab.rowconfigure(3, weight=1)
    
    def populate_database_info(self):
        """Populate the database information tab with styled content."""
        self.db_text.delete(1.0, tk.END)
        
        extensions = sorted(self.detector.database.get_supported_extensions())
        
        # Add header
        header = "File Extensions Supported by Magic Number Detection\n"
        header += "=" * 70 + "\n\n"
        self.db_text.insert(tk.END, header)
        
        # Group extensions by category (simple grouping by first letter)
        current_letter = ''
        col_width = 15
        cols = 4
        
        i = 0
        while i < len(extensions):
            # Check if we need a new letter section
            if extensions[i][0].upper() != current_letter:
                current_letter = extensions[i][0].upper()
                if i > 0:
                    self.db_text.insert(tk.END, "\n")
                self.db_text.insert(tk.END, f"[ {current_letter} ]\n")
            
            # Add extensions in rows
            row = extensions[i:i+cols]
            line = "  ".join(f".{ext:<{col_width}}" for ext in row)
            self.db_text.insert(tk.END, line + "\n")
            i += cols
        
        # Add footer info
        footer = f"\n{'=' * 70}\n"
        footer += f"Total: {len(extensions)} unique file extensions supported\n"
        footer += "Categories include: Documents, Images, Archives, Executables, Media, and more\n"
        self.db_text.insert(tk.END, footer)
        
        self.db_text.config(state=tk.DISABLED)
    
    def browse_file(self):
        """Open file browser dialog."""
        filename = filedialog.askopenfilename(
            title="Select a file to analyze",
            filetypes=[("All Files", "*.*")]
        )
        if filename:
            self.file_path_var.set(filename)
    
    def browse_directory(self):
        """Open directory browser dialog."""
        dirname = filedialog.askdirectory(
            title="Select a directory to analyze"
        )
        if dirname:
            self.dir_path_var.set(dirname)
    
    def analyze_file(self):
        """Analyze a single file with improved UX feedback."""
        file_path = self.file_path_var.get().strip()
        
        if not file_path:
            messagebox.showwarning(
                "No File Selected", 
                "Please select a file to analyze.",
                icon='warning'
            )
            return
        
        if not Path(file_path).exists():
            messagebox.showerror(
                "File Not Found", 
                f"The file does not exist:\n\n{file_path}",
                icon='error'
            )
            return
        
        # Clear previous results
        self.file_results_text.config(state=tk.NORMAL)
        self.file_results_text.delete(1.0, tk.END)
        self.file_results_text.insert(1.0, "🔄 Analyzing file...\nPlease wait...")
        self.file_results_text.config(state=tk.DISABLED)
        
        self.status_var.set("🔄 Analyzing file...")
        self.status_label.configure(foreground=self.COLORS['text_secondary'])
        
        # Run analysis in a separate thread to keep GUI responsive
        thread = threading.Thread(target=self._analyze_file_thread, args=(file_path,))
        thread.daemon = True
        thread.start()
    
    def _analyze_file_thread(self, file_path: str):
        """Thread worker for file analysis."""
        try:
            result = self.detector.detect_file(file_path)
            
            # Format output
            output = "=" * 70 + "\n"
            output += "FILE ANALYSIS RESULTS\n"
            output += "=" * 70 + "\n\n"
            output += str(result) + "\n\n"
            
            if result.is_mismatch:
                output += "⚠️  WARNING: MISMATCH DETECTED!\n"
                output += "=" * 70 + "\n"
                output += "This file may be disguised or corrupted!\n"
                output += "The file extension doesn't match the actual content.\n"
            else:
                output += "✓ File extension matches the detected content.\n"
            
            output += "=" * 70 + "\n"
            
            # Update GUI in main thread
            self.root.after(0, self._update_file_results, output, result.is_mismatch)
            
        except Exception as e:
            error_msg = f"❌ Error analyzing file:\n{str(e)}"
            self.root.after(0, self._update_file_results, error_msg, False)
    
    def _update_file_results(self, text: str, is_mismatch: bool):
        """Update file results in main thread with modern styling."""
        self.file_results_text.config(state=tk.NORMAL)
        self.file_results_text.delete(1.0, tk.END)
        self.file_results_text.insert(tk.END, text)
        self.file_results_text.config(state=tk.DISABLED)
        
        if is_mismatch:
            self.status_var.set("⚠️ Analysis complete - MISMATCH DETECTED!")
            self.status_label.configure(foreground=self.COLORS['danger'])
        else:
            self.status_var.set("✓ Analysis complete - File is authentic")
            self.status_label.configure(foreground=self.COLORS['success'])
    
    def analyze_directory(self):
        """Analyze a directory with improved UX feedback."""
        dir_path = self.dir_path_var.get().strip()
        
        if not dir_path:
            messagebox.showwarning(
                "No Directory Selected", 
                "Please select a directory to analyze.",
                icon='warning'
            )
            return
        
        if not Path(dir_path).exists():
            messagebox.showerror(
                "Directory Not Found", 
                f"The directory does not exist:\n\n{dir_path}",
                icon='error'
            )
            return
        
        # Clear previous results
        self.dir_results_text.config(state=tk.NORMAL)
        self.dir_results_text.delete(1.0, tk.END)
        self.dir_results_text.insert(1.0, "🔄 Scanning directory...\nPlease wait...")
        self.dir_results_text.config(state=tk.DISABLED)
        
        recursive = self.recursive_var.get()
        status_msg = f"🔄 Scanning directory{'(recursive)' if recursive else ''}..."
        self.status_var.set(status_msg)
        self.status_label.configure(foreground=self.COLORS['text_secondary'])
        
        # Run analysis in a separate thread
        thread = threading.Thread(target=self._analyze_directory_thread, args=(dir_path, recursive))
        thread.daemon = True
        thread.start()
    
    def _analyze_directory_thread(self, dir_path: str, recursive: bool):
        """Thread worker for directory analysis."""
        try:
            results = self.detector.detect_directory(dir_path, recursive=recursive)
            
            if not results:
                output = "No files found to analyze."
                self.root.after(0, self._update_dir_results, output, 0)
                return
            
            # Generate report
            report = self.detector.generate_report(results)
            
            # Format detailed results
            output = "=" * 70 + "\n"
            output += f"DIRECTORY ANALYSIS: {dir_path}\n"
            output += f"Recursive: {'Yes' if recursive else 'No'}\n"
            output += "=" * 70 + "\n\n"
            output += report + "\n\n"
            output += "DETAILED RESULTS:\n"
            output += "=" * 70 + "\n\n"
            
            mismatch_count = 0
            for result in results:
                status_icon = "⚠️" if result.is_mismatch else "✓"
                output += f"{status_icon} {result.file_path}\n"
                output += f"   Claimed: .{result.claimed_extension or 'NONE'} | "
                output += f"Detected: .{result.detected_type or 'UNKNOWN'}\n"
                
                if result.is_mismatch:
                    output += "   🚨 MISMATCH DETECTED!\n"
                    mismatch_count += 1
                
                output += "\n"
            
            output += "=" * 70 + "\n"
            
            # Update GUI in main thread
            self.root.after(0, self._update_dir_results, output, mismatch_count)
            
        except Exception as e:
            error_msg = f"❌ Error analyzing directory:\n{str(e)}"
            self.root.after(0, self._update_dir_results, error_msg, 0)
    
    def _update_dir_results(self, text: str, mismatch_count: int):
        """Update directory results in main thread with modern styling."""
        self.dir_results_text.config(state=tk.NORMAL)
        self.dir_results_text.delete(1.0, tk.END)
        self.dir_results_text.insert(tk.END, text)
        self.dir_results_text.config(state=tk.DISABLED)
        
        if mismatch_count > 0:
            self.status_var.set(f"⚠️ Scan complete - {mismatch_count} mismatch(es) found!")
            self.status_label.configure(foreground=self.COLORS['danger'])
        else:
            self.status_var.set("✓ Scan complete - No mismatches found")
            self.status_label.configure(foreground=self.COLORS['success'])
    
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = FileTypeIdentifierGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
