def includeme(config):
    config.add_route('users_list',   '/users')
    config.add_route('users_login',  '/users/login')
    config.add_route('users_detail', '/users/{id:\d+}')
    config.add_route('users_events', '/users/{id:\d+}/events')
    config.add_route('users_bookings', '/users/{id:\d+}/bookings')

    config.add_route('events_list',   '/events')
    config.add_route('events_detail', '/events/{id:\d+}')

    config.add_route('bookings_create', '/bookings')
    config.add_route('bookings_detail', '/bookings/{code}')
    config.add_route('bookings_pay',    '/bookings/{code}/pay')
    config.add_route('bookings_cancel', '/bookings/{code}/cancel')
