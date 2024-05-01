<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-center col-span-3 space-y-4">
                <div class="main-center mx-auto grid grid-cols-2 gap-4">
                    <a class="inline-block py-4 px-6 text-right text-black underline underline-offset-2 text-xl">Following</a>
                    <RouterLink to="feed" class="inline-block py-4 px-6 text-left text-black underline-offset-2 text-xl">Recomendation</RouterLink>
                </div>


            <!-- <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="submitForm" method="post">
                    <div class="p-4">  
                        <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                    </div>

                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                    </div>
                </form>
            </div> -->

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
    name: 'FollowingView',
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
    methods: {
        getFeed() {
            axios
                .get(`/post/following/`)
                .then(response => {
                    console.log('data', response.data)
                    this.posts = response.data.following_posts
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
    },
}
</script>