<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-center col-span-3 space-y-4">
            <div class="main-center mx-auto grid grid-cols-2 gap-4">
                <RouterLink to="following" class="inline-block py-4 px-6 text-right text-black underline-offset-2 hover:text-purple-600">Following</RouterLink>
                <a class="inline-block py-4 px-6 text-left text-black underline underline-offset-2 hover:text-purple-600">Recomendation</a>
            </div>
            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-2 border-t border-gray-100 flex justify-between">
                        <div>
                            <input type="file" ref="file" class="block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-gray-100 file:text-gray-700 hover:file:bg-gray-200">
                        </div>
                        
                        <button class="inline-block py-2 px-4 text-black bg-white border border-gray-200 rounded-lg hover:bg-gray-200">Post</button>
                    </div>
                </form>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                <FeedItem v-bind:post="post" />
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <MayInteresting />
        </div>
    </div>
</template>

<script>
import MayInteresting from '../components/MayInteresting.vue'
import axios from 'axios'
import FeedItem from '../components/FeedItem.vue'


export default {
    name: 'FeedView',

    components: {
        MayInteresting,
        FeedItem,
    },
    data() {
        return {
            posts: [],
            body: '',
        }
    },
    mounted() {
        this.getFeed()
    },
    methods: {
        getFeed() {
            axios
                .get('/post/')
                .then(response => {
                    console.log('data', response.data)
                    this.posts = response.data.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        submitForm() {
            console.log('submitForm', this.body)

            let formData = new FormData()
            formData.append('image', this.$refs.file.files[0])
            formData.append('body', this.body)

            axios
                .post('/post/create/', formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                })
                .then(response => {
                    console.log('data', response.data)

                    this.posts.unshift(response.data)
                    this.body = ''
                    // this.$refs.file.files[0] = null
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        
        deletePost(id) {
            this.posts = this.posts.filter(post => post.id !== id)
        },
    },
}
</script>