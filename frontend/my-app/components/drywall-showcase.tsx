'use client'

import { useState } from 'react'
import axios from 'axios'
import { ChevronLeft, ChevronRight } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

const drywallTechniques = [
  {
    title: "Instalación Básica",
    description: "Técnica fundamental para instalar paneles de tablaroca en paredes y techos.",
    image: "/placeholder.svg?height=400&width=600"
  },
  {
    title: "Acabado Liso",
    description: "Proceso para lograr una superficie perfectamente lisa y sin imperfecciones.",
    image: "/placeholder.svg?height=400&width=600"
  },
  {
    title: "Texturizado",
    description: "Aplicación de diferentes texturas decorativas sobre la superficie de la tablaroca.",
    image: "/placeholder.svg?height=400&width=600"
  },
  {
    title: "Esquinas y Bordes",
    description: "Técnicas para lograr esquinas y bordes perfectos en las instalaciones de tablaroca.",
    image: "/placeholder.svg?height=400&width=600"
  }
]

export function DrywallShowcaseComponent() {
  const [currentIndex, setCurrentIndex] = useState(0)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const nextSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % drywallTechniques.length)
  }

  const prevSlide = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + drywallTechniques.length) % drywallTechniques.length)
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
        const response = await axios.post(
            'http://127.0.0.1:5000/login', 
            { username, password },
            {
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        );
        if (response.status === 200) {
            setIsLoggedIn(true);
            console.log('Sesión iniciada con éxito:', response.data);
        }
        const token = response.data.token;
        console.log("Token:", token);
    } catch (error) {
        console.error('Error al iniciar sesión:', error);
    }
};


  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await axios.post('http://127.0.0.1:5000/register', { username, password })
      if (response.status === 201) {
        setIsLoggedIn(true)
        console.log('Usuario registrado con éxito:', response.data)
      }
    } catch (error) {
      console.error('Error al registrar usuario:', error)
    }
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setUsername('')
    setPassword('')
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900">Instalación en Tablaroca</h1>
          {isLoggedIn ? (
            <Button onClick={handleLogout}>Cerrar Sesión</Button>
          ) : (
            <Tabs defaultValue="login" className="w-[400px]">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="login">Iniciar Sesión</TabsTrigger>
                <TabsTrigger value="register">Registrarse</TabsTrigger>
              </TabsList>
              <TabsContent value="login">
                <Card>
                  <CardHeader>
                    <CardTitle>Iniciar Sesión</CardTitle>
                    <CardDescription>Ingresa tus credenciales para acceder a tu cuenta.</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <form onSubmit={handleLogin}>
                      <div className="space-y-1">
                        <Label htmlFor="username">Nombre de Usuario</Label>
                        <Input 
                          id="username" 
                          type="text" 
                          value={username} 
                          onChange={(e) => setUsername(e.target.value)} 
                          required 
                        />
                      </div>
                      <div className="space-y-1">
                        <Label htmlFor="password">Contraseña</Label>
                        <Input 
                          id="password" 
                          type="password" 
                          value={password} 
                          onChange={(e) => setPassword(e.target.value)} 
                          required 
                        />
                      </div>
                      <Button type="submit" className="w-full mt-4" onSubmit={handleLogin}>Iniciar Sesión</Button>
                    </form>
                  </CardContent>
                </Card>
              </TabsContent>
              <TabsContent value="register">
                <Card>
                  <CardHeader>
                    <CardTitle>Registrarse</CardTitle>
                    <CardDescription>Crea una nueva cuenta para acceder a nuestros servicios.</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <form onSubmit={handleRegister}>
                      <div className="space-y-1">
                        <Label htmlFor="username">Nombre de Usuario</Label>
                        <Input 
                          id="username" 
                          type="text" 
                          value={username} 
                          onChange={(e) => setUsername(e.target.value)} 
                          required 
                        />
                      </div>
                      <div className="space-y-1">
                        <Label htmlFor="password">Contraseña</Label>
                        <Input 
                          id="password" 
                          type="password" 
                          value={password} 
                          onChange={(e) => setPassword(e.target.value)} 
                          required 
                        />
                      </div>
                      <Button type="submit" className="w-full mt-4">Registrarse</Button>
                    </form>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          )}
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <Card className="col-span-1 md:col-span-2">
            <CardHeader>
              <CardTitle>{drywallTechniques[currentIndex].title}</CardTitle>
              <CardDescription>{drywallTechniques[currentIndex].description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="relative">
                <img 
                  src={drywallTechniques[currentIndex].image} 
                  alt={drywallTechniques[currentIndex].title}
                  className="w-full h-[400px] object-cover rounded-lg"
                />
                <Button 
                  variant="outline" 
                  size="icon" 
                  className="absolute top-1/2 left-4 transform -translate-y-1/2"
                  onClick={prevSlide}
                >
                  <ChevronLeft className="h-4 w-4" />
                </Button>
                <Button 
                  variant="outline" 
                  size="icon" 
                  className="absolute top-1/2 right-4 transform -translate-y-1/2"
                  onClick={nextSlide}
                >
                  <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>

          {drywallTechniques.map((technique, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow duration-300">
              <CardHeader>
                <CardTitle>{technique.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <img 
                  src={technique.image} 
                  alt={technique.title}
                  className="w-full h-48 object-cover rounded-lg mb-4"
                />
                <CardDescription>{technique.description}</CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
