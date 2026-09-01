"""
Seed data — mirrors the PRODUCTS array from the NOVA frontend so the
backend and existing UI stay in sync (same ids, names, prices, images).
"""

PRODUCTS = [
    {
        "id": 0, "name": "Quantum X1 Laptop", "category": "Electronics",
        "price": 999, "rating": 4.8, "reviews": 124, "badge": "New",
        "image": "https://vlebazaar.in/image/cache/catalog/818cIclbdKL._SL1500_-1200x1200.jpg.webp",
        "description": "Next-gen AI-powered laptop with 32GB RAM and 1TB SSD. Ultra-slim design with a 14\" 4K OLED display.",
        "stock": 40,
    },
    {
        "id": 1, "name": "Nova Buds Pro", "category": "Audio",
        "price": 249, "rating": 4.7, "reviews": 89, "badge": "Bestseller",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-P2zpaRDHQpMylD2LxNrKLHntxaQBDjBgrl_6eIaW9g&s",
        "description": "Active noise-canceling earbuds with spatial audio, 36h battery, and IPX5 water resistance.",
        "stock": 80,
    },
    {
        "id": 2, "name": "Cyber Watch 3", "category": "Wearables",
        "price": 399, "rating": 4.6, "reviews": 67, "badge": None,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcShCt0b0CoAkgec6Q4ED5YHnSljMapwnCYdjKdUVQmdDA&s=10",
        "description": "Advanced health tracker with ECG, GPS, blood oxygen monitoring, and 7-day battery life.",
        "stock": 55,
    },
    {
        "id": 3, "name": "Graviton Gaming Chair", "category": "Gaming",
        "price": 599, "rating": 4.9, "reviews": 45, "badge": "Limited",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQT8VWvqJvRC9FMKRM6gsXhhvha5JCMg0Z6aXwIFru8g&s=10",
        "description": "Ergonomic gaming chair with built-in cooling, 4D armrests, and immersive RGB lighting.",
        "stock": 15,
    },
    {
        "id": 4, "name": "Neon Charging Dock", "category": "Accessories",
        "price": 79, "rating": 4.3, "reviews": 32, "badge": None,
        "image": "https://www.elstarled.com/wp-content/uploads/2023/10/Types-of-Neon-Signs.webp",
        "description": "Wireless fast-charging dock for phone, watch, and earbuds. Sleek futuristic design.",
        "stock": 120,
    },
    {
        "id": 5, "name": 'Eclipse Monitor 32"', "category": "Electronics",
        "price": 749, "rating": 4.8, "reviews": 56, "badge": "New",
        "image": "http://www.ecomed.com.au/wp-content/uploads/2021/04/eclipse-mini-image.png",
        "description": "4K OLED display with 144Hz refresh rate, HDR1000, and ultra-thin bezels.",
        "stock": 30,
    },
    {
        "id": 6, "name": "Orbit Keyboard", "category": "Electronics",
        "price": 189, "rating": 4.5, "reviews": 78, "badge": None,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXMS3a5Z9oLgPcTLXL44Cku0al63ki9j7PeXdLwqtFJA&s=10",
        "description": "Mechanical keyboard with hot-swap switches, customizable RGB, and a premium aluminum frame.",
        "stock": 60,
    },
    {
        "id": 7, "name": "Aura Smart Glasses", "category": "Wearables",
        "price": 299, "rating": 4.2, "reviews": 23, "badge": "Pre-order",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTcvmQqa-rPdhj1L1t25pB8FgArFxSzPUL7sGw1APK3Qw&s=10",
        "description": "AR glasses with heads-up display, voice assistant, and 8MP camera for hands-free capture.",
        "stock": 10,
    },
    {
        "id": 8, "name": "Pulse Soundbar", "category": "Audio",
        "price": 449, "rating": 4.7, "reviews": 41, "badge": None,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTE2srbKzOlr90rAMT8YLTwPyJ1vHHuYFx-SMQB50Ri9A&s=10",
        "description": "Dolby Atmos soundbar with wireless subwoofer, 360 degree audio, and HDMI eARC.",
        "stock": 25,
    },
    {
        "id": 9, "name": "Vertex Mouse", "category": "Accessories",
        "price": 59, "rating": 4.4, "reviews": 29, "badge": None,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSCruLRM4_mgaJXzq6iq0EJ_pF5bz4Ph299pu-6rY42D2UH9xgfXWJGlA&s=10",
        "description": "Ultra-light gaming mouse with 16K DPI, 8 programmable buttons, and PTFE feet.",
        "stock": 90,
    },
]
