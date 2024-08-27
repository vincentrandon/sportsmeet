function toast() {
    return {
        toasts: [],
        addToast(toast) {
            toast.id = Date.now()
            toast.visible = true
            this.toasts.push(toast)
            setTimeout(() => {
                this.removeToast(toast.id)
            }, 5000)
        },
        removeToast(id) {
            const index = this.toasts.findIndex(t => t.id === id)
            if (index > -1) {
                this.toasts[index].visible = false
                setTimeout(() => {
                    this.toasts.splice(index, 1)
                }, 300)
            }
        },
        updateToasts() {
            // This function is called whenever the toasts array changes
            // You can add any additional logic here if needed
        }
    }
}