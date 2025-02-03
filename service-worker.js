self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('street-smart-cache').then((cache) => {
            return cache.addAll([
                '/',
                '/static/css/style.css',
                '/static/icons/icon-192x192.png'
            ]);
        })
    );
});