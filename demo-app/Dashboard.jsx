import React, { useState, useEffect } from 'react';

/**
 * FreshCart Dashboard — Order History & Account Overview
 *
 * INTENTIONAL MIX of good and bad patterns for Hermes Clew demo:
 * - Some semantic elements, some div-soup
 * - Some accessible patterns, some missing ARIA
 * - Showcases what the scanner catches in JSX files
 */

function Dashboard() {
    const [orders, setOrders] = useState([]);
    const [notifications, setNotifications] = useState([]);

    useEffect(() => {
        fetch('/api/orders').then(r => r.json()).then(setOrders);
        fetch('/api/notifications').then(r => r.json()).then(setNotifications);
    }, []);

    return (
        <div className="dashboard">

            {/* GOOD: semantic heading hierarchy */}
            <h1>My Dashboard</h1>

            {/* BAD: nav links inside plain div, not <nav> */}
            <div className="dashboard-tabs">
                <div className="tab" onClick={() => setActiveTab('orders')}>Orders</div>
                <div className="tab" onClick={() => setActiveTab('favorites')}>Favorites</div>
                <div className="tab" onClick={() => setActiveTab('settings')}>Settings</div>
            </div>

            {/* BAD: notification area without aria-live */}
            <div className="notifications-panel">
                {notifications.map(n => (
                    <div key={n.id} className="notification-item">
                        {/* BAD: icon-only dismiss button without aria-label */}
                        <span className="dismiss" onClick={() => dismissNotification(n.id)}>✕</span>
                        <p>{n.message}</p>
                    </div>
                ))}
            </div>

            {/* GOOD: uses <section> */}
            <section>
                <h2>Recent Orders</h2>

                {/* BAD: divs as list items instead of <ul>/<li> */}
                {orders.map(order => (
                    <div key={order.id} className="order-card">
                        <div className="order-header">
                            <span>Order #{order.id}</span>
                            <span>{order.date}</span>
                        </div>
                        <div className="order-items">
                            {order.items.map(item => (
                                <div key={item.name} className="order-item-row">
                                    {/* BAD: image without alt text */}
                                    <img src={item.thumbnail} />
                                    <span>{item.name}</span>
                                    <span>${item.price}</span>
                                </div>
                            ))}
                        </div>
                        {/* BAD: div with onClick instead of <button> */}
                        <div className="reorder-btn" onClick={() => reorder(order.id)}>
                            Reorder
                        </div>
                        {/* GOOD: proper anchor with href */}
                        <a href={`/orders/${order.id}/details`}>View full order details</a>
                    </div>
                ))}
            </section>

            <section>
                <h2>Quick Actions</h2>
                {/* GOOD: proper <button> elements */}
                <button onClick={() => navigate('/products')}>Browse Products</button>
                <button onClick={() => navigate('/deals')}>Today's Deals</button>

                {/* BAD: div with onClick instead of button */}
                <div className="action-card" onClick={() => navigate('/referral')}>
                    Refer a Friend — Get $10 Off
                </div>
            </section>

            {/* BAD: entire section is div-soup with no semantic structure */}
            <div className="account-summary">
                <div className="summary-title">Account Summary</div>
                <div className="summary-row">
                    <div className="label">Member Since</div>
                    <div className="value">January 2025</div>
                </div>
                <div className="summary-row">
                    <div className="label">Total Orders</div>
                    <div className="value">{orders.length}</div>
                </div>
                <div className="summary-row">
                    <div className="label">Rewards Points</div>
                    <div className="value">2,450</div>
                </div>
            </div>

        </div>
    );
}

export default Dashboard;
