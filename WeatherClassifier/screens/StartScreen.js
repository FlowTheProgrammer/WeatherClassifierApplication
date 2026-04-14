import { View, Text, StyleSheet, TouchableOpacity, Dimensions, ScrollView } from 'react-native';
import { useCameraPermissions } from 'expo-camera';
import * as MediaLibrary from 'expo-media-library';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useState } from 'react';

const {height} = Dimensions.get('window');

const Portions = [
    {
        icon: '⛈️',
        title: 'Weather From Photo',
        body: 'Take a photo of the sky or upload an image, the app will analyze the image and predict the weather condition.',
        bg: '#1c3d5a',
    },
    {
        icon: '🌡️',
        title: 'Dectects 11 Types of Conditions',
        body: 'Can detect 11 different weather conditions, including sunny, cloudy, rainy, snowy, foggy, and more.',
        bg: '#1c3d5a',
    },
    {
        icon: '📸',
        title: 'Camera Needed',
        body: 'Permissions will be asked prior to upload.',
        bg: '#1c3d5a',
    },
]

export default function StartScreen({ navigation}){

    const [portion, setPortion] = useState(0);
    const [cameraPermission, requestCameraPermission] = useCameraPermissions();

    const current = Portions[portion]
    const isLast = portion === Portions.length -1;

    const handleNext = async () => {
        if (current.needsPermission){
            await requestCameraPermission();
            await MediaLibrary.requestPermissionsAsync();
        }
        if (isLast){
            await AsyncStorage.setItem('onboarded', 'true');
            navigation.navigate('Home');
        } else {
            setPortion(portion + 1);
        }
    };

    return (
        < View style={[styles.container, {backgroundColor: current.bg}]}>
            <View style={styles.inner}>
                <View style={styles.dots}>
                    {Portions.map((_,i)=> (
                        <View key={i} style={[styles.dot, i === portion && styles.activeDot]} />
                    ))}
                </View>
                <Text style={styles.icon}>{current.icon}</Text>
                <Text style={styles.title}>{current.title}</Text>
                <Text style={styles.body}>{current.body}</Text>
            </View>

        <View style={styles.footer}>
            <TouchableOpacity onPress={handleNext} style={styles.button}>
                <Text style={styles.buttonText}>{isLast ? 'Get Started' : 'Next'}</Text>
            </TouchableOpacity>
            {!isLast && (
                <TouchableOpacity onPress={async () => {
                    await AsyncStorage.setItem('onboarded', 'true');
                    navigation.navigate('Home');
                }}>
                    <Text style={styles.skip}>Skip</Text>
                    </TouchableOpacity>
            )}
        </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    inner: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 32,
    },
    icon: {
        fontSize: 72,
        marginBottom: 28,
    },
    title: {
        fontSize: 26,
        fontWeight: '500',
        color: 'white',
        textAlign: 'center',
        marginBottom: 12,
        lineHeight: 32,
    },
    dots: {
        flexDirection: 'row',
        
    },
    dot:{
        width: 6,
        height: 6,
        borderRadius: 3,
        backgroundColor: '#fff',
    },
    activeDot: {
        backgroundColor: 'white',
        width: 20,
        borderRadius: 3
    },
    body: {
        fontSize: 15,
        color: '#fff',
        textAlign: 'center',
        lineHeight: 23,
    },
    footer: {
        padding: 28,
        paddingBottom: 48,
        gap: 14
    },
    button:{
        backgroundColor: 'black',
        padding: 16,
        borderWidth: 0.5,
        alignItems: 'center',
        borderColor: 'rbga(255,255,255,255,0.35'
    },
    buttonText: {
        color: 'white',
        fontSize: 16,
        fontWeight: '500',

    },
    skip: {
        color: 'black',
        textAlign: 'center',
        fontSize: 14,
    }
});


