# 🎨 MovieRecs Frontend - Styling Guide

## Cinema Theme Design System

### Color Palette

**Primary Colors:**
- **Yellow**: `#FBBF24` (`text-yellow-400`, `bg-yellow-500`) - CTAs, highlights, stars
- **Purple**: `#9333EA` (`bg-purple-600`, `to-purple-600`) - Primary buttons, gradients
- **Indigo**: `#4F46E5` (`bg-indigo-600`) - Secondary actions
- **Orange**: `#F97316` (`bg-orange-500`, `to-orange-500`) - Accents, transitions

**Background:**
- **Black**: `#000000` - Main background
- **Dark Gray**: `#111827` - Cards, containers (gray-900)
- **Medium Gray**: `#1F2937` - Hover states (gray-800)
- **Light Gray**: `#9CA3AF` - Text secondary (gray-400)

**Text:**
- **White**: `#FFFFFF` - Primary text
- **Gray-300**: `#D1D5DB` - Secondary text
- **Gray-400**: `#9CA3AF` - Tertiary text
- **Gray-500**: `#6B7280` - Disabled state

### Typography

```tailwind
/* Headings */
h1: text-5xl font-black
h2: text-4xl font-black
h3: text-2xl font-bold
h4: text-xl font-bold

/* Body */
p: text-base/lg font-normal
strong: font-bold
em: italic

/* Special */
.text-yellow-400: For emphasis/CTAs
.bg-clip-text.text-transparent: For gradient text
```

### Gradient Usage

**Hero Gradients:**
```tailwind
from-black via-gray-900 to-black
from-indigo-900 via-purple-900 to-black
from-gray-900 to-gray-800
from-purple-600 to-indigo-600
from-yellow-500 to-orange-500
```

**Text Gradients:**
```tailwind
bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent
bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent
bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent
```

**Button Gradients:**
```tailwind
from-yellow-500 to-orange-500      /* Primary CTA */
from-purple-600 to-indigo-600      /* Secondary */
from-red-600 to-pink-600           /* Danger */
from-green-600 to-emerald-600      /* Success */
```

### Component Styles

#### MovieCard
```tailwind
relative bg-gradient-to-br from-gray-900 to-gray-800
rounded-xl overflow-hidden shadow-xl
hover:shadow-2xl transition-all duration-300
h-64 (or h-80)

/* Overlay gradient */
absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent
absolute inset-0 group-hover:bg-black/20 transition-colors

/* Title */
font-bold text-lg text-white
group-hover:text-yellow-400 transition-colors
line-clamp-2

/* Rating badge */
text-xs bg-yellow-500 text-black px-2 py-1 rounded font-bold
★ 8.5
```

#### Button Styles

**Primary CTA:**
```tailwind
px-8 py-3 bg-gradient-to-r from-yellow-500 to-orange-500
text-black font-bold rounded-lg
hover:shadow-lg hover:shadow-yellow-500/50 transition-all
transform hover:scale-105
```

**Secondary Button:**
```tailwind
px-6 py-2 bg-gradient-to-r from-purple-600 to-indigo-600
text-white font-bold rounded-lg
hover:shadow-lg transition-all
disabled:opacity-50 disabled:cursor-not-allowed
```

**Danger Button:**
```tailwind
px-4 py-2 bg-red-600 hover:bg-red-700
text-white font-bold rounded-lg transition-all
```

#### Form Inputs

```tailwind
/* Text inputs */
w-full p-3 bg-gray-800 border border-gray-700
rounded-lg text-white placeholder-gray-500
focus:border-yellow-500 focus:outline-none
transition-colors

/* Select dropdowns */
w-full p-3 bg-gray-800 border border-gray-700
rounded-lg text-white
focus:border-yellow-500 focus:outline-none
transition-colors
```

#### Cards/Containers

```tailwind
bg-gradient-to-br from-gray-900 to-gray-800
p-8 rounded-xl
border border-purple-500/20
shadow-xl

/* Alternative */
bg-gradient-to-r from-gray-900 to-gray-800
p-6 rounded-xl
border border-gray-700
hover:border-yellow-500/50 transition-all
```

#### Headers/Sections

```tailwind
text-4xl font-black
bg-gradient-to-r from-yellow-400 to-pink-500
bg-clip-text text-transparent
```

### Animation & Transition

**All Interactive Elements:**
```tailwind
transition-all
transition-colors
transition-all duration-300
```

**Hover Effects:**
```tailwind
/* Scale */
transform hover:scale-105

/* Shadow */
hover:shadow-lg
hover:shadow-yellow-500/50

/* Color */
group-hover:text-yellow-400 transition-colors

/* Opacity */
hover:opacity-80

/* Combined */
transform hover:scale-105 transition-all
```

**Loading States:**
```tailwind
animate-pulse
h-64 bg-gray-800 rounded-xl animate-pulse
```

### Spacing & Layout

**Container Widths:**
```tailwind
max-w-7xl mx-auto px-4
max-w-4xl mx-auto px-4
max-w-2xl mx-auto px-4
```

**Grid Layouts:**
```tailwind
/* Movies grid - responsive */
grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6

/* Profile sections */
grid-cols-1 md:grid-cols-2 gap-8

/* Stats cards */
grid-cols-2 gap-6
```

**Padding Standards:**
```tailwind
py-12        /* Page vertical padding */
px-4         /* Page horizontal padding */
p-8          /* Card padding */
p-6          /* Section padding */
p-4          /* Small section padding */
```

### Border & Shadow

**Borders:**
```tailwind
border border-purple-500/20      /* Subtle */
border-2 border-red-500/30       /* Danger zone */
border-t border-gray-700         /* Divider */
border-b border-purple-500/20    /* Bottom */
```

**Shadows:**
```tailwind
shadow-xl                        /* Base */
hover:shadow-2xl                 /* Hover */
hover:shadow-yellow-500/50       /* Colored */
```

### Responsive Considerations

**Mobile First:**
```tailwind
/* Base mobile, then override */
grid-cols-1              /* Mobile */
sm:grid-cols-2           /* Tablet */
md:grid-cols-3           /* Small desktop */
lg:grid-cols-4           /* Desktop */
```

**Text Sizing:**
```tailwind
text-4xl              /* Mobile headers */
sm:text-5xl           /* Desktop headers */
text-base             /* Mobile body */
lg:text-lg            /* Desktop body */
```

**Spacing:**
```tailwind
py-8 lg:py-12
px-4 lg:px-8
gap-4 md:gap-6 lg:gap-8
```

### Special Effects

**Gradient Text:**
```jsx
className="bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent"
```

**Glow Effect:**
```tailwind
hover:shadow-lg hover:shadow-yellow-500/50
```

**Fade Overlay:**
```tailwind
absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent
```

**Blur Background:**
```tailwind
absolute inset-0 opacity-30
<div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-screen filter blur-3xl"></div>
```

### Dark Mode Compatibility

All components designed for **dark mode by default**:
- Black backgrounds
- White/light gray text
- Yellow/orange accents for visibility
- High contrast for accessibility

### Accessibility

**Color Contrast:**
- Text on black: white/light gray (WCAG AAA)
- Yellow on black: excellent contrast
- Disabled states: reduced opacity with `opacity-50`

**Interactive Elements:**
- Clear hover states
- Focus outlines (e.g., `focus:border-yellow-500 focus:outline-none`)
- Readable font sizes (min `text-base`)

### Brand Colors Quick Reference

| Use Case | Color | Tailwind |
|----------|-------|----------|
| CTAs | Yellow | `bg-yellow-500 text-black` |
| Primary Buttons | Purple-Indigo | `from-purple-600 to-indigo-600` |
| Danger | Red | `bg-red-600` |
| Success | Green | `bg-green-600` |
| Accents | Orange | `bg-orange-500` |
| Highlights | Pink | `to-pink-500` (in gradients) |
| Backgrounds | Black/Gray | `bg-black` / `from-gray-900` |
| Text Primary | White | `text-white` |
| Text Secondary | Gray-300 | `text-gray-300` |

---

**Theme**: 🎬 Cinema  
**Mood**: Modern, Bold, Cinematic  
**Inspiration**: Netflix, Movie theaters, Modern web apps
