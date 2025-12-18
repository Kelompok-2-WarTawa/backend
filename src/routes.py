def includeme(config):
    config.add_route('users_list',    '/api/users')
    config.add_route('users_login',   '/api/users/login')
    config.add_route('users_detail', r'/api/users/{id:\d+}')
    config.add_route('users_events', r'/api/users/{id:\d+}/events')
    config.add_route('users_bookings', r'/api/users/{id:\d+}/bookings')

    config.add_route('events_list',    '/api/events')
    config.add_route('events_detail', r'/api/events/{id:\d+}')

    config.add_route('events_seats', r'/api/events/{id:\d+}/seats')

    config.add_route('bookings_create', '/api/bookings')
    config.add_route('bookings_detail', '/api/bookings/{code}')
    config.add_route('bookings_pay',    '/api/bookings/{code}/pay')
    config.add_route('bookings_cancel', '/api/bookings/{code}/cancel')
