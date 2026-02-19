// Minimal frontend JS for Campus Service Hub
// Handles auth, fetch wrappers and page-specific actions (vanilla JS)

const apiFetch = async (path, { method = 'GET', body = null, isForm = false } = {}) => {
  const headers = {};
  const token = localStorage.getItem('token');
  if (token) headers['Authorization'] = 'Bearer ' + token;
  if (!isForm) headers['Content-Type'] = 'application/json';
  const res = await fetch('/api' + path, {
    method,
    headers,
    body: isForm ? body : body ? JSON.stringify(body) : null,
  });
  if (res.status === 401) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw data;
  return data;
};

const showUserInNav = (user) => {
  document.getElementById('login-link').style.display = user ? 'none' : 'inline';
  document.getElementById('signup-link').style.display = user ? 'none' : 'inline';
  document.getElementById('logout-link').style.display = user ? 'inline' : 'none';
  document.getElementById('user-info').textContent = user ? (user.name + ' (' + user.role + ')') : '';
  document.getElementById('admin-link').style.display = (user && user.role === 'admin') ? 'inline' : 'none';
  document.getElementById('profile-link').style.display = user ? 'inline' : 'none';
};

// small toast notification helper
const toastWrap = (() => {
  let el = document.querySelector('.toast-wrap');
  if (!el) { el = document.createElement('div'); el.className = 'toast-wrap'; document.body.appendChild(el); }
  return el;
})();

function showToast(message, type = 'info', timeout = 3000) {
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.textContent = message;
  toastWrap.appendChild(t);
  // force reflow to enable transition
  requestAnimationFrame(() => t.classList.add('show'));
  setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 220); }, timeout);
}

const loadCurrentUser = async () => {
  const token = localStorage.getItem('token');
  if (!token) { showUserInNav(null); return null; }
  try {
    const resp = await fetch('/api/auth/me', { headers: { 'Authorization': 'Bearer ' + token } });
    if (!resp.ok) throw 1;
    const data = await resp.json();
    localStorage.setItem('user', JSON.stringify(data.user));
    showUserInNav(data.user);
    return data.user;
  } catch (err) {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    showUserInNav(null);
    return null;
  }
};

// Auth handlers
document.addEventListener('DOMContentLoaded', async () => {
  await loadCurrentUser();
  attachGlobalHandlers();
  routePageInit();
  // run home init if present
  if (document.getElementById('homeAnnouncements')) initHomePage();
});

function attachGlobalHandlers() {
  const logout = document.getElementById('logout-link');
  if (logout) logout.addEventListener('click', (e) => { e.preventDefault(); localStorage.removeItem('token'); localStorage.removeItem('user'); showUserInNav(null); window.location = '/'; });

  const loginForm = document.getElementById('loginForm');
  if (loginForm) loginForm.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    try {
      const res = await fetch('/api/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email, password }) });
      const data = await res.json();
      if (!res.ok) throw data;
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      showUserInNav(data.user);
      showToast('Login successful', 'success');
      window.location = '/';
    } catch (err) {
      showToast(err.detail || 'Login failed', 'error');
    }
  });

  const signupForm = document.getElementById('signupForm');
  if (signupForm) signupForm.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    try {
      const res = await fetch('/api/auth/signup', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ name, email, password }) });
      const data = await res.json();
      if (!res.ok) throw data;
      alert('Account created');
      window.location = '/login';
    } catch (err) {
      showToast(err.detail || 'Signup failed', 'error');
    }
  });
}

// Page routing / initialization
async function routePageInit() {
  if (document.getElementById('complaintForm')) await initComplaintsPage();
  if (document.getElementById('eventsList')) await initEventsPage();
  if (document.getElementById('bookingForm')) await initBookingsPage();
  if (document.getElementById('annList')) await initAnnouncementsPage();
  if (document.getElementById('usersCount')) await initDashboardPage();
  if (document.getElementById('profileForm')) await initProfilePage();
}

// Complaints
async function initComplaintsPage() {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const form = document.getElementById('complaintForm');

  // only students can submit complaints
  if (!user || user.role !== 'student') {
    form.style.display = 'none';
    const note = document.createElement('div');
    note.className = 'muted';
    note.textContent = 'You must be logged in as a student to submit complaints.';
    form.parentNode.insertBefore(note, form);
  } else {
    form.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const fd = new FormData();
      fd.append('title', document.getElementById('title').value);
      fd.append('description', document.getElementById('description').value);
      fd.append('category', document.getElementById('category').value);
      const f = document.getElementById('image').files[0];
      if (f) fd.append('file', f);
      try {
        await apiFetch('/complaints/', { method: 'POST', body: fd, isForm: true });
        showToast('Complaint submitted', 'success');
        loadMyComplaints();
      } catch (err) { showToast(err.detail || 'Failed', 'error'); }
    });
  }

  loadMyComplaints();

  // admin-only: load all complaints
  if (user && user.role === 'admin') {
    document.getElementById('allComplaintsSection').style.display = 'block';
    loadAllComplaints();
  }
}

async function loadMyComplaints() {
  try {
    const res = await apiFetch('/complaints/me');
    const ul = document.getElementById('complaintsList');
    ul.innerHTML = '';
    res.forEach(c => {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${c.title}</strong> — <em>${c.category}</em> <div>${c.description}</div><div>Status: ${c.status}</div>${c.image_path ? `<div><img src='${c.image_path}' style='max-width:180px'></div>` : ''}`;
      ul.appendChild(li);
    });
  } catch (err) { console.error(err); }
}

async function loadAllComplaints() {
  try {
    const res = await apiFetch('/complaints/');
    const ul = document.getElementById('allComplaintsList');
    ul.innerHTML = '';
    res.forEach(c => {
      const li = document.createElement('li');
      li.innerHTML = `<div style='display:flex;justify-content:space-between;gap:12px;align-items:center'><div><strong>${c.title}</strong><div class='muted'>by user #${c.user_id} — ${c.category}</div><div>${c.description}</div>${c.image_path? `<div><img src='${c.image_path}' style='max-width:120px'></div>`: ''}</div><div style='text-align:right'>Status: <strong>${c.status}</strong><div style='margin-top:8px'><select data-id='${c.id}' class='status-select'><option value='pending'>pending</option><option value='in_progress'>in_progress</option><option value='resolved'>resolved</option></select><button data-id='${c.id}' class='btn btn-ghost update-status' style='margin-top:6px'>Update</button></div></div></div>`;
      ul.appendChild(li);
    });
    // attach handlers
    document.querySelectorAll('.update-status').forEach(btn => {
      btn.addEventListener('click', async (ev) => {
        const id = btn.getAttribute('data-id');
        const sel = document.querySelector(`.status-select[data-id='${id}']`);
        const status = sel.value;
        try {
          const form = new FormData();
          form.append('status', status);
          await fetch(`/api/complaints/${id}/status`, { method: 'PUT', headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }, body: form });
          showToast('Updated', 'success');
          loadAllComplaints();
        } catch (err) { showToast('Failed to update', 'error'); }
      });
    });
  } catch (err) { console.error(err); }
}

// Events
async function initEventsPage() {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  if (user && user.role === 'admin') document.getElementById('createEventSection').style.display = 'block';
  document.getElementById('eventForm')?.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const payload = {
      title: document.getElementById('title').value,
      date: document.getElementById('date').value,
      venue: document.getElementById('venue').value,
      capacity: parseInt(document.getElementById('capacity').value, 10),
      description: document.getElementById('description').value,
    };
    try {
      await apiFetch('/events/', { method: 'POST', body: payload });
      showToast('Event created', 'success');
      loadEvents();
    } catch (err) { showToast(err.detail || 'Failed', 'error'); }
  });
  loadEvents();
}

async function loadEvents() {
  // get current user's registrations (if authenticated) so we can mark buttons
  let registeredSet = new Set();
  try {
    const reg = await apiFetch('/events/registrations/me');
    registeredSet = new Set(reg.event_ids || []);
  } catch (err) {
    // not authenticated or no registrations
    registeredSet = new Set();
  }

  try {
    const res = await apiFetch('/events/');
    const ul = document.getElementById('eventsList');
    ul.innerHTML = '';
    res.forEach(e => {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${e.title}</strong> — <em>${new Date(e.date).toLocaleString()}</em> <div>${e.venue} | Capacity: ${e.capacity}</div><div>${e.description || ''}</div>`;
      const btn = document.createElement('button');
      // mark button disabled if already registered
      if (registeredSet.has(e.id)) {
        btn.textContent = 'Registered';
        btn.disabled = true;
        btn.className = 'btn';
      } else {
        btn.textContent = 'Register';
        btn.onclick = async () => {
          const user = JSON.parse(localStorage.getItem('user') || 'null');
          if (!user) { showToast('Please login to register', 'error'); return; }
          try {
            await apiFetch(`/events/${e.id}/register`, { method: 'POST' });
            btn.textContent = 'Registered';
            btn.disabled = true;
            showToast('Registered', 'success');
          } catch (err) { showToast(err.detail || 'Failed to register', 'error'); }
        };
      }
      li.appendChild(btn);
      ul.appendChild(li);
    });
  } catch (err) { console.error(err); }
}

// Bookings
async function initBookingsPage() {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  const form = document.getElementById('bookingForm');

  // only students can request bookings
  if (!user || user.role !== 'student') {
    form.style.display = 'none';
    const note = document.createElement('div');
    note.className = 'muted';
    note.textContent = 'You must be logged in as a student to request room bookings.';
    form.parentNode.insertBefore(note, form);
  } else {
    document.getElementById('bookingForm')?.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const payload = {
        room_name: document.getElementById('room_name').value,
        date: document.getElementById('date').value,
        start_time: document.getElementById('start_time').value,
        end_time: document.getElementById('end_time').value,
      };
      try {
        await apiFetch('/bookings/', { method: 'POST', body: payload });
        showToast('Booking requested', 'success');
        loadBookings();
      } catch (err) { showToast(err.detail || 'Failed to create booking', 'error'); }
    });
  }

  loadBookings();

  // admin: show all bookings
  if (user && user.role === 'admin') {
    document.getElementById('allBookingsSection').style.display = 'block';
    loadAllBookings();
  }
}

async function loadBookings() {
  try {
    const res = await apiFetch('/bookings/me');
    const ul = document.getElementById('bookingsList');
    ul.innerHTML = '';
    res.forEach(b => {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${b.room_name}</strong> — ${b.date} ${b.start_time} - ${b.end_time} <div>Status: ${b.status}</div>`;
      ul.appendChild(li);
    });
  } catch (err) { console.error(err); }
}

async function loadAllBookings() {
  try {
    const res = await apiFetch('/bookings/');
    const ul = document.getElementById('allBookingsList');
    ul.innerHTML = '';
    res.forEach(b => {
      const li = document.createElement('li');
      li.innerHTML = `<div style='display:flex;justify-content:space-between;gap:12px;align-items:center'><div><strong>${b.room_name}</strong><div class='muted'>by user #${b.user_id}</div><div>${b.date} ${b.start_time}-${b.end_time}</div></div><div style='text-align:right'>Status: <strong>${b.status}</strong><div style='margin-top:8px'><button data-id='${b.id}' class='btn btn-ghost approve'>Approve</button> <button data-id='${b.id}' class='btn btn-ghost reject'>Reject</button></div></div></div>`;
      ul.appendChild(li);
    });
    document.querySelectorAll('.approve').forEach(btn => btn.addEventListener('click', async () => { const id = btn.getAttribute('data-id'); try { await apiFetch(`/bookings/${id}/status`, { method: 'PUT', body: { status: 'approved' } }); showToast('Approved', 'success'); loadAllBookings(); } catch (err) { showToast('Failed', 'error'); }}));
    document.querySelectorAll('.reject').forEach(btn => btn.addEventListener('click', async () => { const id = btn.getAttribute('data-id'); try { await apiFetch(`/bookings/${id}/status`, { method: 'PUT', body: { status: 'rejected' } }); showToast('Rejected', 'success'); loadAllBookings(); } catch (err) { showToast('Failed', 'error'); }}));
  } catch (err) { console.error(err); }
}

// Announcements
async function initAnnouncementsPage() {
  const user = JSON.parse(localStorage.getItem('user') || 'null');
  if (user && user.role === 'admin') document.getElementById('createAnn').style.display = 'block';
  document.getElementById('annForm')?.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    const fd = new FormData();
    fd.append('title', document.getElementById('title').value);
    fd.append('content', document.getElementById('content').value);
    try {
      await fetch('/api/announcements/', { method: 'POST', headers: { 'Authorization': 'Bearer ' + localStorage.getItem('token') }, body: fd });
      showToast('Posted', 'success');
      loadAnnouncements();
    } catch (err) { showToast('Failed', 'error'); }
  });
  loadAnnouncements();
}

async function loadAnnouncements() {
  try {
    const res = await apiFetch('/announcements/');
    const ul = document.getElementById('annList');
    ul.innerHTML = '';
    res.forEach(a => {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${a.title}</strong> <div>${a.content}</div><div><small>${new Date(a.created_at).toLocaleString()}</small></div>`;
      ul.appendChild(li);
    });
  } catch (err) { console.error(err); }
}

// Admin Dashboard
async function initDashboardPage() {
  // copy / login buttons for admin
  const copyBtn = document.getElementById('copy-admin-creds');
  const loginBtn = document.getElementById('login-as-admin');
  const exportBtn = document.getElementById('export-report');
  if (copyBtn) copyBtn.addEventListener('click', () => {
    const creds = 'admin@example.com:admin123';
    navigator.clipboard?.writeText(creds).then(() => showToast('Credentials copied', 'success')).catch(() => showToast('Copy failed', 'error'));
  });
  if (loginBtn) loginBtn.addEventListener('click', async () => {
    loginBtn.disabled = true;
    try {
      const res = await fetch('/api/auth/login', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ email: 'admin@example.com', password: 'admin123' }) });
      const data = await res.json();
      if (!res.ok) throw data;
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      showUserInNav(data.user);
      showToast('Logged in as admin', 'success');
      setTimeout(() => window.location.reload(), 600);
    } catch (err) {
      showToast(err.detail || 'Login failed', 'error');
      loginBtn.disabled = false;
    }
  });
  if (exportBtn) exportBtn.addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    if (!token) { showToast('Login as admin first', 'error'); return; }
    try {
      const resp = await fetch('/api/admin/dashboard/export', { headers: { 'Authorization': 'Bearer ' + token } });
      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw err;
      }
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'chattan_report.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) { showToast(err.detail || 'Export failed', 'error'); }
  });

  try {
    const stats = await apiFetch('/admin/dashboard/stats');
    document.getElementById('usersCount').textContent = stats.users;
    document.getElementById('complaintsCount').textContent = stats.complaints;
    document.getElementById('eventsCount').textContent = stats.events;
    document.getElementById('bookingsCount').textContent = stats.bookings;

    const recent = await apiFetch('/admin/dashboard/recent');
    const ul = document.getElementById('recentList');
    ul.innerHTML = '';
    recent.recent.forEach(r => {
      const li = document.createElement('li');
      li.innerHTML = `<div><strong>${r.title}</strong><div class='muted kind'>${r.kind}</div></div><div class='muted'>${new Date(r.created_at).toLocaleString()}</div>`;
      ul.appendChild(li);
    });
  } catch (err) { console.error(err); }
}

// Profile page
async function initProfilePage() {
  const token = localStorage.getItem('token');
  if (!token) {
    showToast('Please login to edit profile', 'error');
    return;
  }
  try {
    const res = await apiFetch('/profile/');
    const user = res;
    document.getElementById('p_name').value = user.name || '';
    document.getElementById('p_email').value = user.email || '';
    document.getElementById('p_phone').value = user.phone || '';
    if (user.role === 'admin') document.getElementById('profileAdminActions').style.display = 'block';

    document.getElementById('profileForm').addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const payload = { name: document.getElementById('p_name').value, email: document.getElementById('p_email').value, phone: document.getElementById('p_phone').value };
      try {
        const resp = await apiFetch('/profile/', { method: 'PUT', body: payload });
        showToast('Profile updated', 'success');
        showUserInNav(resp.user);
        // refresh profile events after update
        loadProfileEvents();
      } catch (err) { showToast(err.detail || 'Update failed', 'error'); }
    });

    document.getElementById('passwordForm').addEventListener('submit', async (ev) => {
      ev.preventDefault();
      const payload = { old_password: document.getElementById('old_password').value, new_password: document.getElementById('new_password').value };
      try {
        await apiFetch('/profile/change-password', { method: 'POST', body: payload });
        showToast('Password changed', 'success');
        document.getElementById('old_password').value = '';
        document.getElementById('new_password').value = '';
      } catch (err) { showToast(err.detail || 'Password change failed', 'error'); }
    });

    document.getElementById('profileExport')?.addEventListener('click', async () => {
      try {
        const resp = await fetch('/api/admin/dashboard/export', { headers: { 'Authorization': 'Bearer ' + token } });
        if (!resp.ok) { const e = await resp.json().catch(() => ({})); throw e; }
        const blob = await resp.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url; a.download = 'chattan_report.pdf'; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
      } catch (err) { showToast(err.detail || 'Export failed', 'error'); }
    });

    // load the user's events for the profile view
    await loadProfileEvents();

  } catch (err) {
    showToast('Could not load profile', 'error');
  }
}

async function loadProfileEvents() {
  try {
    const res = await apiFetch('/profile/events');
    const up = document.getElementById('profileUpcoming');
    const past = document.getElementById('profilePast');
    up.innerHTML = '';
    past.innerHTML = '';
    res.upcoming.forEach(e => { const li = document.createElement('li'); li.innerHTML = `<strong>${e.title}</strong> — <span class='muted'>${new Date(e.date).toLocaleString()}</span>`; up.appendChild(li); });
    res.past.forEach(e => { const li = document.createElement('li'); li.innerHTML = `<strong>${e.title}</strong> — <span class='muted'>${new Date(e.date).toLocaleString()}</span>`; past.appendChild(li); });
  } catch (err) { /* ignore */ }
}

// Home page: load announcements, events and stats
async function initHomePage() {
  try {
    const res = await apiFetch('/home/summary');
    const ann = document.getElementById('homeAnnouncements');
    const ev = document.getElementById('homeEvents');
    const st = document.getElementById('homeStats');
    if (ann) {
      ann.innerHTML = '';
      res.announcements.forEach(a => { const li = document.createElement('li'); li.innerHTML = `<strong>${a.title}</strong><div class='muted'>${new Date(a.created_at).toLocaleString()}</div>`; ann.appendChild(li); });
    }
    if (ev) {
      ev.innerHTML = '';
      res.events.forEach(e => { const li = document.createElement('li'); li.innerHTML = `<strong>${e.title}</strong> — <span class='muted'>${new Date(e.date).toLocaleString()}</span>`; ev.appendChild(li); });
    }
    if (st) st.textContent = `Users: ${res.stats.users} • Events: ${res.stats.events} • Complaints: ${res.stats.complaints} • Bookings: ${res.stats.bookings}`;
  } catch (err) { console.error(err); }
}

