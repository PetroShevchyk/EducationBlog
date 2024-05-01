<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-center col-span-3 space-y-4">
            <div class="rounded-lg">
                <h2 class="text-xl text-center">Category: #{{ $route.params.id }}</h2>
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
        }
    },
    mounted() {
        this.getFeed()
    },
    watch: { 
        '$route.params.id': {
            handler: function() {
                this.getFeed()
            },
            deep: true,
            immediate: true
        }
    },
    methods: {
        getFeed() {
            axios
                .get(`/post/?category=${this.$route.params.id}`)
                .then(response => {
                    this.posts = []
                    console.log('data', response.data)
                    this.posts = response.data.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    },
}
</script>