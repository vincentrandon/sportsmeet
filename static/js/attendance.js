window.attendanceFunctions = {
    confirmAttendance(attendanceId) {
        fetch(`/confirm-attendance-manual/${attendanceId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.getCsrfToken(),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.showToast('Présence confirmée avec succès', 'success');
                this.openPanel = null;
                location.reload();
            } else {
                this.showToast('Erreur lors de la confirmation de la présence: ' + data.message, 'error');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            this.showToast('Erreur lors de la confirmation de la présence', 'error');
        });
    },
    sendConfirmationEmail(attendanceId) {
        fetch(`/send-confirmation-email/${attendanceId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': this.getCsrfToken(),
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                this.showToast('Email envoyé avec succès', 'success');
                this.openPanel = null;
                location.reload();
            } else if (data.status === 'info') {
                this.showToast(data.message, 'info');
            } else {
                this.showToast('Erreur lors de l\'envoi de l\'email: ' + data.message, 'error');
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            this.showToast('Erreur lors de l\'envoi de l\'email', 'error');
        });
    },
    removeAttendance(attendanceId) {
        if (confirm('Êtes-vous sûr de vouloir supprimer cette présence ?')) {
            fetch(`/remove-attendance/${attendanceId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken(),
                    'Content-Type': 'application/json',
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    this.showToast('Présence supprimée avec succès', 'success');
                    this.openPanel = null;
                    location.reload();
                } else {
                    this.showToast('Erreur lors de la suppression de la présence: ' + data.message, 'error');
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                this.showToast('Erreur lors de la suppression de la présence', 'error');
            });
        }
    },
    getCsrfToken() {
        return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    },
    showToast(message, type) {
        console.log(`${type.toUpperCase()}: ${message}`);
        // Implement a more stylish toast notification here
    }
};

// Initialize Alpine.js component
document.addEventListener('alpine:init', () => {
    Alpine.data('attendanceActions', () => ({
        openPanel: null,
        ...window.attendanceFunctions
    }));
});