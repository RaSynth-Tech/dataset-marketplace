import React, { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function LoginCallback() {
    const { handleLoginCallback } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const token = params.get('access_token');
        const userStr = params.get('user');

        if (token && userStr) {
            try {
                const user = JSON.parse(userStr);
                handleLoginCallback(token, user);
                navigate('/');
            } catch (e) {
                console.error('Failed to parse user data', e);
                navigate('/');
            }
        } else {
            navigate('/');
        }
    }, [location, handleLoginCallback, navigate]);

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
            <div className="text-center">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">Logging you in...</h2>
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            </div>
        </div>
    );
}

export default LoginCallback;
