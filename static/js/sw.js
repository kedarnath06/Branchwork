/**
 * Service Worker for Bangla Sentiment Analysis
 * Provides offline capabilities and caching
 */

const CACHE_NAME = 'bangla-sentiment-v1.0';
const STATIC_CACHE = 'static-v1.0';
const API_CACHE = 'api-v1.0';

// Resources to cache immediately
const PRECACHE_URLS = [
    '/',
    '/static/css/main.css',
    '/static/js/main.js',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'
];

// Install event - cache static resources
self.addEventListener('install', event => {
    console.log('Service Worker: Installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(cache => {
                console.log('Service Worker: Caching static files');
                return cache.addAll(PRECACHE_URLS);
            })
            .then(() => {
                console.log('Service Worker: Static files cached');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('Service Worker: Caching failed', error);
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker: Activating...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (cacheName !== STATIC_CACHE && cacheName !== API_CACHE) {
                            console.log('Service Worker: Deleting old cache', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker: Activated');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Handle API requests
    if (url.pathname.startsWith('/api/')) {
        event.respondWith(handleApiRequest(request));
        return;
    }
    
    // Handle static files and pages
    event.respondWith(
        caches.match(request)
            .then(cachedResponse => {
                if (cachedResponse) {
                    console.log('Service Worker: Serving from cache', request.url);
                    return cachedResponse;
                }
                
                console.log('Service Worker: Fetching from network', request.url);
                return fetch(request)
                    .then(response => {
                        // Clone the response
                        const responseClone = response.clone();
                        
                        // Cache successful responses
                        if (response.status === 200) {
                            caches.open(STATIC_CACHE)
                                .then(cache => {
                                    cache.put(request, responseClone);
                                });
                        }
                        
                        return response;
                    })
                    .catch(error => {
                        console.error('Service Worker: Network request failed', error);
                        
                        // Return offline page for navigation requests
                        if (request.mode === 'navigate') {
                            return caches.match('/');
                        }
                        
                        throw error;
                    });
            })
    );
});

// Handle API requests with network-first strategy
async function handleApiRequest(request) {
    try {
        // Try network first
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            // Cache successful API responses
            const cache = await caches.open(API_CACHE);
            cache.put(request, networkResponse.clone());
            
            console.log('Service Worker: API response cached', request.url);
        }
        
        return networkResponse;
        
    } catch (error) {
        console.log('Service Worker: Network failed, trying cache', error);
        
        // Try cache as fallback
        const cachedResponse = await caches.match(request);
        
        if (cachedResponse) {
            console.log('Service Worker: Serving API from cache', request.url);
            return cachedResponse;
        }
        
        // Return offline response for API requests
        return new Response(
            JSON.stringify({
                error: 'Offline',
                message: 'You are currently offline. Please check your connection and try again.',
                success: false
            }),
            {
                status: 503,
                statusText: 'Service Unavailable',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );
    }
}

// Handle background sync for offline analysis requests
self.addEventListener('sync', event => {
    if (event.tag === 'background-sentiment-analysis') {
        console.log('Service Worker: Background sync triggered');
        event.waitUntil(handleBackgroundSync());
    }
});

async function handleBackgroundSync() {
    // Handle any queued sentiment analysis requests
    // This would be implemented based on your specific requirements
    console.log('Service Worker: Processing background sync');
}

// Handle push notifications (if needed in the future)
self.addEventListener('push', event => {
    console.log('Service Worker: Push received');
    
    const options = {
        body: event.data ? event.data.text() : 'New update available',
        icon: '/static/images/favicon.svg',
        badge: '/static/images/badge.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: '1'
        },
        actions: [
            {
                action: 'explore',
                title: 'View Details',
                icon: '/static/images/checkmark.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/static/images/close.png'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('Bangla Sentiment Analysis', options)
    );
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    console.log('Service Worker: Notification clicked');
    
    event.notification.close();
    
    if (event.action === 'explore') {
        // Open the app
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Handle messages from the main thread
self.addEventListener('message', event => {
    console.log('Service Worker: Message received', event.data);
    
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'GET_VERSION') {
        event.ports[0].postMessage({ version: CACHE_NAME });
    }
});

// Periodic background sync (experimental)
self.addEventListener('periodicsync', event => {
    if (event.tag === 'update-cache') {
        console.log('Service Worker: Periodic sync triggered');
        event.waitUntil(updateCache());
    }
});

async function updateCache() {
    console.log('Service Worker: Updating cache');
    
    const cache = await caches.open(STATIC_CACHE);
    
    try {
        await cache.addAll(PRECACHE_URLS);
        console.log('Service Worker: Cache updated successfully');
    } catch (error) {
        console.error('Service Worker: Cache update failed', error);
    }
}

console.log('Service Worker: Script loaded');