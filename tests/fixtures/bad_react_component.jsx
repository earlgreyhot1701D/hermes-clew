import React from 'react';

function ContactPage() {
    const handleSubmit = () => { /* submit logic */ };
    const navigate = (path) => { window.location.href = path; };

    return (
        <div className="page">
            <div className="navbar">
                <div className="nav-item" onClick={() => navigate('/')}>Home</div>
                <div className="nav-item" onClick={() => navigate('/about')}>About</div>
                <div className="nav-item" onClick={() => navigate('/contact')}>Contact</div>
            </div>

            <div className="title" style={{fontSize: '32px'}}>Contact Us</div>

            <div className="form-area">
                <span>Full Name</span>
                <input placeholder="Enter name" />

                <span>Email</span>
                <input placeholder="Enter email" />

                <span>Message</span>
                <div contentEditable={true} className="fake-textarea"></div>

                <div className="btn" onClick={handleSubmit}>Send Message</div>
            </div>

            <div className="section">
                <div className="subtitle">Our Offices</div>
                <div className="list">
                    <div className="list-item">San Francisco, CA</div>
                    <div className="list-item">New York, NY</div>
                    <div className="list-item">London, UK</div>
                </div>
            </div>

            <img src="/map.png" />
        </div>
    );
}

export default ContactPage;
