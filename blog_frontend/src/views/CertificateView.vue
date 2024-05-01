<template>
    <button @click="$router.back()" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 m-4 rounded-lg">
    Back
    </button>
    <div class="flex justify-center">
        <img :src="user.get_certificate">
    </div>
    
</template>
<script>
import axios from 'axios'

export default {
    name: 'CertificateView',
    data() {
        return {
            user: {
                id: null,
            }
        }
    },
    mounted() {
        this.getFeed()
    },
    methods: {
        getFeed() {
                axios
                    .get(`/api/certificate/${this.$route.params.id}/`)
                    .then(response => {
                        console.log('data', response.data)
                        this.user = response.data
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            },
    },
}
</script>