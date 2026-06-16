import customtkinter as ctk

class ToastItem(ctk.CTkFrame):
    """
    Modern floating toast notification item.
    """
    STYLES = {
        "error": {
            "accent": ("#E11D48", "#F43F5E"),
            "card_bg": ("#FFFFFF", "#141221"),
            "border": ("#FDA4AF", "#F43F5E"),
            "title": ("#881337", "#FFFFFF"),
            "description": ("#475569", "#CBD5E1"),
            "icon": "⚠️",
            "icon_bg": ("#FFE4E6", "#3B1018"),
            "icon_text": ("#E11D48", "#FDA4AF"),
            "close_text": ("#64748B", "#94A3B8"),
            "close_hover": ("#FFE4E6", "#26233A"),
            "progress_track": ("#FFE4E6", "#2A263C"),
        },
        "warning": {
            "accent": ("#F59E0B", "#F59E0B"),
            "card_bg": ("#FFFBEB", "#141221"),
            "border": ("#FBBF24", "#F59E0B"),
            "title": ("#78350F", "#FFFFFF"),
            "description": ("#475569", "#CBD5E1"),
            "icon": "⚡",
            "icon_bg": ("#FEF3C7", "#3B2F08"),
            "icon_text": ("#D97706", "#FCD34D"),
            "close_text": ("#64748B", "#94A3B8"),
            "close_hover": ("#FEF3C7", "#26233A"),
            "progress_track": ("#FEF3C7", "#2A263C"),
        },
        "success": {
            "accent": ("#22C55E", "#22C55E"),
            "card_bg": ("#F0FDF4", "#141221"),
            "border": ("#86EFAC", "#22C55E"),
            "title": ("#14532D", "#FFFFFF"),
            "description": ("#475569", "#CBD5E1"),
            "icon": "✅",
            "icon_bg": ("#DCFCE7", "#082F1A"),
            "icon_text": ("#16A34A", "#86EFAC"),
            "close_text": ("#64748B", "#94A3B8"),
            "close_hover": ("#DCFCE7", "#26233A"),
            "progress_track": ("#DCFCE7", "#2A263C"),
        },
        "info": {
            "accent": ("#3B82F6", "#38BDF8"),
            "card_bg": ("#EFF6FF", "#141221"),
            "border": ("#93C5FD", "#38BDF8"),
            "title": ("#1E3A8A", "#FFFFFF"),
            "description": ("#475569", "#CBD5E1"),
            "icon": "ℹ️",
            "icon_bg": ("#DBEAFE", "#0C1929"),
            "icon_text": ("#2563EB", "#93C5FD"),
            "close_text": ("#64748B", "#94A3B8"),
            "close_hover": ("#DBEAFE", "#26233A"),
            "progress_track": ("#DBEAFE", "#2A263C"),
        },
    }

    def __init__(self, master, message, toast_type="error", title=None, duration=7000, on_dismiss=None, **kwargs):
        self.toast_type = toast_type
        style = self.STYLES.get(toast_type, self.STYLES["error"])

        super().__init__(
            master, 
            fg_color=style["card_bg"], 
            border_color=style["border"], 
            border_width=1, 
            corner_radius=16, 
            width=430, 
            height=110, 
            **kwargs
        )
        self.pack_propagate(False)

        self.on_dismiss = on_dismiss
        self.duration = duration
        self._after_id = None
        self._progress_after_id = None
        self._elapsed = 0
        self._is_paused = False
        
        # Content Frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=16, pady=12)

        # Icon
        icon_label = ctk.CTkLabel(content_frame, text=style["icon"], font=("Segoe UI", 24), text_color=style["icon_text"])
        icon_label.pack(side="left", padx=(0, 12), anchor="n")

        # Text Frame
        text_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True)

        if title:
            ctk.CTkLabel(text_frame, text=title, font=("Segoe UI", 14, "bold"), text_color=style["title"], anchor="w").pack(fill="x", anchor="w")
        
        if message:
            # allow multi-line wrapping
            ctk.CTkLabel(text_frame, text=message, font=("Segoe UI", 12), text_color=style["description"], anchor="w", justify="left", wraplength=320).pack(fill="x", expand=True, anchor="w")

        # Close Button
        close_btn = ctk.CTkButton(
            content_frame, text="×", width=24, height=24, corner_radius=12,
            fg_color="transparent", hover_color=style["close_hover"], text_color=style["close_text"],
            font=("Segoe UI", 16, "bold"), command=self.dismiss
        )
        close_btn.pack(side="right", anchor="ne")

        # Progress Bar Frame (Bottom)
        self.progress_bg = ctk.CTkFrame(self, fg_color="transparent", height=3, corner_radius=0)
        self.progress_bg.place(relx=0, rely=1.0, anchor="sw", relwidth=1.0, y=-1)
        
        self.progress_bar = ctk.CTkFrame(self.progress_bg, fg_color=style["accent"], height=3, corner_radius=0)
        self.progress_bar.place(relx=0, rely=0, relwidth=1.0)

        # Hover events to pause timer
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
        for child in self.winfo_children():
            self._bind_hover_recursive(child)

        # Start timer
        if self.duration:
            self._update_progress()

    def _bind_hover_recursive(self, widget):
        widget.bind("<Enter>", self._on_hover, add="+")
        widget.bind("<Leave>", self._on_leave, add="+")
        for child in widget.winfo_children():
            self._bind_hover_recursive(child)

    def _on_hover(self, event):
        self._is_paused = True

    def _on_leave(self, event):
        self._is_paused = False

    def _update_progress(self):
        if not self.winfo_exists():
            return
            
        if not self._is_paused:
            self._elapsed += 50
            if self._elapsed >= self.duration:
                self.dismiss()
                return
            
            # Update progress bar width
            remaining_ratio = 1.0 - (self._elapsed / self.duration)
            self.progress_bar.place_configure(relwidth=max(0, remaining_ratio))
            
        self._progress_after_id = self.after(50, self._update_progress)

    def dismiss(self, immediate=False):
        if self._progress_after_id:
            try:
                self.after_cancel(self._progress_after_id)
            except Exception:
                pass
            self._progress_after_id = None
            
        try:
            self.pack_forget()
        except Exception:
            pass

        if self.on_dismiss:
            try:
                self.on_dismiss(self)
            except Exception:
                pass

        try:
            self.destroy()
        except Exception:
            pass

class ToastManager:
    """
    Global manager for floating toast notifications.
    Positions toasts at the top right of the application window.
    """
    def __init__(self, root):
        self.root = root
        self.toasts = []
        self.max_toasts = 3
        self.container = None

    def _ensure_container(self):
        if self.container is not None:
            try:
                if self.container.winfo_exists():
                    return
            except Exception:
                pass
            self.container = None

        self.container = ctk.CTkFrame(
            self.root, 
            fg_color="transparent",
            width=1,
            height=1,
            corner_radius=0,
            border_width=0
        )
        self.container.place(relx=1.0, y=22, x=-24, anchor="ne")
        self.container.lift()

    def _cleanup_container_if_empty(self):
        if len(self.toasts) > 0:
            return
            
        if self.container is not None:
            try:
                self.container.place_forget()
            except Exception:
                pass
                
            try:
                self.container.destroy()
            except Exception:
                pass
                
            self.container = None

    def show(self, message=None, toast_type="error", title=None, description=None, duration=None):
        if not duration:
            duration = 7000 if toast_type == "error" else 5000

        # Use description as message if message is None but description is provided
        msg_text = message if message is not None else description

        self._ensure_container()

        # Enforce max toasts
        while len(self.toasts) >= self.max_toasts:
            oldest_toast = self.toasts.pop(0)
            oldest_toast.dismiss(immediate=True)

        # Create new toast
        toast = ToastItem(
            self.container, 
            message=msg_text, 
            toast_type=toast_type, 
            title=title, 
            duration=duration,
            on_dismiss=self._on_toast_dismiss
        )
        
        pady_top = 0 if len(self.toasts) == 0 else 10
        self.toasts.append(toast)
        toast.pack(pady=(pady_top, 0), anchor="ne", fill="x")
        
        # Ensure container stays on top
        try:
            self.container.lift()
        except Exception:
            pass
            
        return toast

    def _on_toast_dismiss(self, toast):
        if toast in self.toasts:
            self.toasts.remove(toast)
            
        self._repack_toasts()
        self._cleanup_container_if_empty()

    def _repack_toasts(self):
        for index, toast in enumerate(list(self.toasts)):
            try:
                toast.pack_forget()
                toast.pack(fill="x", pady=(0 if index == 0 else 10, 0), anchor="ne")
            except Exception:
                pass
