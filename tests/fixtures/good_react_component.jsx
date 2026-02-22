import React from 'react';

function ContactPage() {
    return (
        <main>
            <nav aria-label="Main navigation">
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>

            <h1>Contact Us</h1>

            <form action="/api/contact" method="post">
                <label htmlFor="name">Full Name</label>
                <input type="text" id="name" name="name" required aria-required="true" />

                <label htmlFor="email">Email</label>
                <input type="email" id="email" name="email" required aria-required="true" />

                <label htmlFor="message">Message</label>
                <textarea id="message" name="message" aria-required="true"></textarea>

                <button type="submit">Send Message</button>
            </form>

            <section aria-label="Office locations">
                <h2>Our Offices</h2>
                <ul>
                    <li>San Francisco, CA</li>
                    <li>New York, NY</li>
                    <li>London, UK</li>
                </ul>
            </section>

            <img src="/map.png" alt="Map showing office locations" />
        </main>
    );
}

export default ContactPage;
