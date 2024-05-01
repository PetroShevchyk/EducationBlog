<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" class="p-4 flex space-x-4">  
                    <input v-model="query" type="search" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you looking for?">

                    <button class="inline-block py-2 px-4 text-black bg-white border border-gray-200 rounded-lg hover:bg-gray-200">Search</button>
                </form>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-4 gap-4" v-if="users.length">
                
                <div class="p-4 text-center bg-gray-100 rounded-lg" v-for="user in users" v-bind:key="user.id">
                    <img :src="user.get_avatar" class="mb-6 rounded-full">
                
                    <p><strong><RouterLink :to="{name: 'profile', params: {'id': user.id}}">{{ user.name }}</RouterLink></strong></p>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
                        <p class="text-xs text-gray-500">{{ user.posts_count }} posts</p>
                    </div>
                </div>
            </div>

            <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                <FeedItem v-bind:post="post"/>
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
    name: 'SearchView',

    components: {
        MayInteresting,
        FeedItem,
    },

    data() {
        return {
            query: '',
            users: [],
            posts: [],
        }
    },

    methods: {
        submitForm() {
            console.log('submitForm', this.query)

            axios
                .post('/search/', {
                    'query': this.query
                })
                .then(response => {
                    console.log('response:', response.data)

                    this.users = response.data.users
                    this.posts = response.data.posts
                })
                .catch(error => {
                    console.log('error:', error)
                })
        },
    },
}
</script>